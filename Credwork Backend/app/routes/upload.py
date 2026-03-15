"""
Upload routes — returns data matching exact frontend contracts.

POST /upload/statement
  Response: { upload_id, status, mode, gigscore, gigscore_label, certificate_id,
              months_found, platforms_found, monthly_avg, ... }
  Frontend passes the full response to ProcessingScreen → SuccessScreen.

GET /upload/status/{upload_id}
  Same response shape so the polling fallback also works.
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.config.database import get_supabase
from app.routes.auth import get_current_user

router = APIRouter(tags=["upload"])
TEMP_DIR = os.getenv("TEMP", "/tmp")
os.makedirs(TEMP_DIR, exist_ok=True)


def _load_upload_dependencies():
    # Import heavy PDF/ML modules lazily so a serverless cold start can still
    # boot the API even if optional native deps are unavailable.
    from app.utils.fraud import run_fraud_checks
    from app.utils.vpa_parser import (
        extract_all_credits,
        classify_transactions,
        aggregate_by_month,
    )
    from app.utils.gigscore import calculate_gigscore
    from app.utils.conflict_resolver import resolve_and_save_income
    from app.utils.cert_generator import generate_certificate
    from app.ml.anomaly_detector import detect_income_anomalies, get_anomaly_severity

    return {
        "run_fraud_checks": run_fraud_checks,
        "extract_all_credits": extract_all_credits,
        "classify_transactions": classify_transactions,
        "aggregate_by_month": aggregate_by_month,
        "calculate_gigscore": calculate_gigscore,
        "resolve_and_save_income": resolve_and_save_income,
        "generate_certificate": generate_certificate,
        "detect_income_anomalies": detect_income_anomalies,
        "get_anomaly_severity": get_anomaly_severity,
    }


def _build_upload_response(upload_id: str, upload_row: dict, gigscore: int = 0,
                            gigscore_label: str = "Insufficient", certificate_id=None,
                            months_found: int = 0, platforms_found: list = None,
                            monthly_avg: int = 0, anomaly: dict = None,
                            mode: str = "gig",
                            period_start: str = None, period_end: str = None,
                            version: int = 1) -> dict:
    """
    Builds the standard upload response shape that both the upload POST
    and the status GET return. Matches what ProcessingScreen/SuccessScreen expect.
    """
    return {
        "upload_id": str(upload_id),
        "status": upload_row.get("status", "processing"),
        "mode": mode,
        # GigScore — matches SuccessScreen params
        "gigscore": gigscore,
        "gigscore_label": gigscore_label,
        # Certificate
        "certificate_id": certificate_id,
        # Income summary
        "months_found": months_found,
        "platforms_found": platforms_found or [],
        "monthly_avg": monthly_avg,
        # Period from actual transactions
        "period_start": period_start,
        "period_end": period_end,
        "version": version,
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
    deps = _load_upload_dependencies()

    if user["role"] != "gig_worker":
        raise HTTPException(403, "Only gig workers can upload bank statements.")

    if file.content_type not in ["application/pdf", "application/x-pdf"]:
        raise HTTPException(400, "File must be a PDF.")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large. Maximum size is 10MB.")

    db = get_supabase()

    # ── Save to temp ────────────────────────────────────────────
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.pdf")
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
        fraud_result = deps["run_fraud_checks"](temp_path)

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

        # ── Extract ALL credits + classify ────────────────────
        all_txns = deps["extract_all_credits"](temp_path)
        gig_txns, credit_txns = deps["classify_transactions"](all_txns)

        # ── Mode Decision ─────────────────────────────────────
        if gig_txns:
            mode = "gig"
            income_txns = gig_txns
        elif credit_txns:
            mode = "generic"
            income_txns = credit_txns
        else:
            # No credits at all — true invalid
            os.remove(temp_path)
            db.table("pdf_uploads").update({
                "status": "failed",
                "fraud_check": "passed",
                "fraud_reason": "No credit transactions found in this PDF.",
                "processed_at": "now()"
            }).eq("id", upload_id).execute()

            raise HTTPException(422, {
                "status": "failed",
                "mode": "invalid",
                "reason": "No credit transactions found. Please upload a bank statement with income credits.",
                "upload_id": str(upload_id)
            })

        # ── Aggregate income ──────────────────────────────────
        by_platform, monthly_totals = deps["aggregate_by_month"](income_txns)

        # ── Resolve conflicts & save income entries ───────────
        await deps["resolve_and_save_income"](user["id"], by_platform, upload_id, db)

        # ── Cleanup temp file ─────────────────────────────────
        os.remove(temp_path)

        # ── ML Anomaly detection ──────────────────────────────
        monthly_amounts = [monthly_totals.get(m, 0) for m in sorted(monthly_totals.keys())]
        anomaly_result = deps["detect_income_anomalies"](monthly_amounts)
        severity = deps["get_anomaly_severity"](anomaly_result)

        if severity == "high":
            try:
                db.table("fraud_flags").insert({
                    "worker_id": user["id"],
                    "upload_id": upload_id,
                    "flag_type": "ml_anomaly_high",
                    "flag_reason": anomaly_result["reason"] or "ML model detected high-severity anomaly.",
                }).execute()
            except Exception as ff_err:
                print(f"[upload] Could not insert fraud flag (table may be missing): {ff_err}")

        # Store ML results on the upload record (columns may not exist yet)
        try:
            db.table("pdf_uploads").update({
                "ml_anomaly_detected": anomaly_result["anomaly_detected"],
                "ml_anomaly_score": min(anomaly_result["anomaly_scores"]) if anomaly_result["anomaly_scores"] else None,
                "ml_model_confidence": anomaly_result["model_confidence"],
                "ml_anomaly_note": anomaly_result["reason"],
            }).eq("id", upload_id).execute()
        except Exception as ml_err:
            print(f"[upload] Could not save ML results (columns may be missing): {ml_err}")

        # ── GigScore (works for both modes — measures consistency) ──
        gigscore_result = deps["calculate_gigscore"](monthly_totals)

        # ── Certificate ───────────────────────────────────────
        months_count = len([m for m, amt in monthly_totals.items() if amt > 0])
        cert_id = None
        if months_count >= 3:
            cert_id = await deps["generate_certificate"](user["id"], gigscore_result, db, mode=mode)

        # ── Build summary fields ──────────────────────────────
        platforms_found = sorted(set(t["platform"] for t in income_txns if t.get("platform")))
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

        # Compute actual period from transaction months
        sorted_months_list = sorted(monthly_totals.keys())
        p_start = sorted_months_list[0] if sorted_months_list else None
        p_end = sorted_months_list[-1] if sorted_months_list else None

        # Get certificate version
        cert_version = 1
        if cert_id:
            cert_row = db.table("certificates").select("version").eq("cert_id", cert_id).limit(1).execute()
            if cert_row.data:
                cert_version = cert_row.data[0].get("version", 1)

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
            mode=mode,
            period_start=p_start,
            period_end=p_end,
            version=cert_version,
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
    gigscore, gigscore_label, cert_id, monthly_avg, mode = 0, "Insufficient", None, 0, "gig"

    if row["status"] in ("passed", "flagged"):
        cert = (
            db.table("certificates")
            .select("cert_id, gigscore, gigscore_label, monthly_avg_inr, mode")
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
            mode = cert.data[0].get("mode", "gig")

    return _build_upload_response(
        upload_id=upload_id,
        upload_row=row,
        gigscore=gigscore,
        gigscore_label=gigscore_label,
        certificate_id=cert_id,
        months_found=row.get("months_found") or 0,
        platforms_found=row.get("platforms_found") or [],
        monthly_avg=monthly_avg,
        mode=mode,
    )
