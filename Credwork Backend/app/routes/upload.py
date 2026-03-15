"""
Upload routes — returns data matching exact frontend contracts.

POST /upload/statement
  Response: { upload_id, status, gigscore, gigscore_label, certificate_id,
              months_found, platforms_found, monthly_avg, ... }
  Frontend passes the full response to ProcessingScreen → SuccessScreen.

GET /upload/status/{upload_id}
  Same response shape so the polling fallback also works.
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.config.database import get_supabase
from app.utils.fraud import run_fraud_checks
from app.utils.vpa_parser import extract_gig_income, aggregate_by_month
from app.utils.gigscore import calculate_gigscore
from app.utils.conflict_resolver import resolve_and_save_income
from app.utils.cert_generator import generate_certificate
from app.ml.anomaly_detector import detect_income_anomalies, get_anomaly_severity
from app.routes.auth import get_current_user

router = APIRouter(tags=["upload"])
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

VPA_CONFIG = "app/config/vpa_config.json"


def _build_upload_response(upload_id: str, upload_row: dict, gigscore: int = 0,
                            gigscore_label: str = "Insufficient", certificate_id=None,
                            months_found: int = 0, platforms_found: list = None,
                            monthly_avg: int = 0, anomaly: dict = None) -> dict:
    """
    Builds the standard upload response shape that both the upload POST
    and the status GET return. Matches what ProcessingScreen/SuccessScreen expect.
    """
    return {
        "upload_id": str(upload_id),
        "status": upload_row.get("status", "processing"),
        # GigScore — matches SuccessScreen params
        "gigscore": gigscore,
        "gigscore_label": gigscore_label,
        # Certificate
        "certificate_id": certificate_id,
        # Income summary
        "months_found": months_found,
        "platforms_found": platforms_found or [],
        "monthly_avg": monthly_avg,
        # Fraud
        "fraud_check": upload_row.get("fraud_check"),
        "fraud_reason": upload_row.get("fraud_reason"),
        # ML
        "ml_anomaly_detected": anomaly.get("anomaly_detected", False) if anomaly else False,
        "ml_anomaly_note": anomaly.get("reason") if anomaly else None,
        "ml_model_confidence": anomaly.get("model_confidence", 0) if anomaly else 0,
    }


@router.post("/upload/statement")
async def upload_statement(file: UploadFile = File(...), user=Depends(get_current_user)):
    if user["role"] != "gig_worker":
        raise HTTPException(403, "Only gig workers can upload bank statements.")

    if file.content_type not in ["application/pdf", "application/x-pdf"]:
        raise HTTPException(400, "File must be a PDF.")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large. Maximum size is 10MB.")

    db = get_supabase()

    # ── Save to temp ────────────────────────────────────────────
    temp_path = f"{TEMP_DIR}/{uuid.uuid4()}.pdf"
    with open(temp_path, "wb") as f:
        f.write(content)

    # ── Create upload record ─────────────────────────────────
    upload_result = db.table("pdf_uploads").insert({
        "worker_id": user["id"],
        "status": "processing"
    }).execute()
    upload_id = upload_result.data[0]["id"]
    upload_row = upload_result.data[0]

    try:
        # ── Fraud check ──────────────────────────────────────
        fraud_result = run_fraud_checks(temp_path)

        if not fraud_result["passed"]:
            os.remove(temp_path)
            db.table("pdf_uploads").update({
                "status": "failed",
                "fraud_check": "failed",
                "fraud_reason": fraud_result["reason"],
                "processed_at": "now()"
            }).eq("id", upload_id).execute()

            raise HTTPException(422, {
                "status": "failed",
                "fraud_check": "failed",
                "reason": fraud_result["reason"],
                "upload_id": str(upload_id)
            })

        # ── Extract + aggregate income ────────────────────────
        transactions = extract_gig_income(temp_path, VPA_CONFIG)
        by_platform, monthly_totals = aggregate_by_month(transactions)

        if not transactions:
            os.remove(temp_path)
            db.table("pdf_uploads").update({
                "status": "failed",
                "fraud_check": "passed",
                "fraud_reason": "No gig income transactions found.",
                "processed_at": "now()"
            }).eq("id", upload_id).execute()

            raise HTTPException(422, {
                "status": "failed",
                "reason": "No gig platform payments found. Make sure this is a bank statement with Swiggy, Zomato, Uber, or similar credits.",
                "upload_id": str(upload_id)
            })

        # ── Resolve conflicts & save income entries ───────────
        await resolve_and_save_income(user["id"], by_platform, upload_id, db)

        # ── Cleanup temp file ─────────────────────────────────
        os.remove(temp_path)

        # ── ML Anomaly detection ──────────────────────────────
        monthly_amounts = [monthly_totals.get(m, 0) for m in sorted(monthly_totals.keys())]
        anomaly_result = detect_income_anomalies(monthly_amounts)
        severity = get_anomaly_severity(anomaly_result)

        if severity == "high":
            db.table("fraud_flags").insert({
                "worker_id": user["id"],
                "upload_id": upload_id,
                "flag_type": "ml_anomaly_high",
                "flag_reason": anomaly_result["reason"] or "ML model detected high-severity anomaly.",
            }).execute()

        # Store ML results on the upload record
        db.table("pdf_uploads").update({
            "ml_anomaly_detected": anomaly_result["anomaly_detected"],
            "ml_anomaly_score": min(anomaly_result["anomaly_scores"]) if anomaly_result["anomaly_scores"] else None,
            "ml_model_confidence": anomaly_result["model_confidence"],
            "ml_anomaly_note": anomaly_result["reason"],
        }).eq("id", upload_id).execute()

        # ── GigScore ──────────────────────────────────────────
        gigscore_result = calculate_gigscore(monthly_totals)

        # ── Certificate ───────────────────────────────────────
        months_count = len([m for m, amt in monthly_totals.items() if amt > 0])
        cert_id = None
        if months_count >= 3:
            cert_id = await generate_certificate(user["id"], gigscore_result, db)

        # ── Build summary fields ──────────────────────────────
        platforms_found = sorted(set(t["platform"] for t in transactions))
        monthly_avg = round(sum(monthly_totals.values()) / max(len(monthly_totals), 1))

        # ── Final update to upload record ─────────────────────
        final_status = "flagged" if fraud_result.get("flagged") else "passed"
        db.table("pdf_uploads").update({
            "status": final_status,
            "fraud_check": "flagged" if fraud_result.get("flagged") else "passed",
            "months_found": months_count,
            "platforms_found": platforms_found,
            "processed_at": "now()"
        }).eq("id", upload_id).execute()

        upload_row["status"] = final_status
        upload_row["fraud_check"] = upload_row.get("fraud_check", "passed")

        return _build_upload_response(
            upload_id=upload_id,
            upload_row=upload_row,
            gigscore=gigscore_result["score"],
            gigscore_label=gigscore_result["label"],
            certificate_id=cert_id,
            months_found=months_count,
            platforms_found=platforms_found,
            monthly_avg=monthly_avg,
            anomaly=anomaly_result,
        )

    except HTTPException:
        raise
    except Exception as e:
        # Catch-all — mark upload as failed
        if os.path.exists(temp_path):
            os.remove(temp_path)
        db.table("pdf_uploads").update({
            "status": "failed",
            "fraud_reason": str(e),
            "processed_at": "now()"
        }).eq("id", upload_id).execute()
        raise HTTPException(500, f"Processing failed: {str(e)}")


@router.get("/upload/status/{upload_id}")
async def get_upload_status(upload_id: str, user=Depends(get_current_user)):
    """
    Returns upload status — same shape as the POST response
    so the frontend can poll and navigate to SuccessScreen with the same data.
    """
    db = get_supabase()
    result = (
        db.table("pdf_uploads")
        .select("*")
        .eq("id", upload_id)
        .eq("worker_id", user["id"])
        .execute()
    )

    if not result.data:
        raise HTTPException(404, "Upload not found.")

    row = result.data[0]

    # Fetch gigscore from the certificate if upload is passed
    gigscore, gigscore_label, cert_id, monthly_avg = 0, "Insufficient", None, 0

    if row["status"] in ("passed", "flagged"):
        cert = (
            db.table("certificates")
            .select("cert_id, gigscore, gigscore_label, monthly_avg_inr")
            .eq("worker_id", user["id"])
            .eq("status", "active")
            .order("generated_at", desc=True)
            .limit(1)
            .execute()
        )
        if cert.data:
            gigscore = cert.data[0]["gigscore"]
            gigscore_label = cert.data[0]["gigscore_label"]
            cert_id = cert.data[0]["cert_id"]
            monthly_avg = cert.data[0]["monthly_avg_inr"]

    return _build_upload_response(
        upload_id=upload_id,
        upload_row=row,
        gigscore=gigscore,
        gigscore_label=gigscore_label,
        certificate_id=cert_id,
        months_found=row.get("months_found") or 0,
        platforms_found=row.get("platforms_found") or [],
        monthly_avg=monthly_avg,
    )
