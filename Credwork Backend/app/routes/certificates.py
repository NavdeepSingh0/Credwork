"""
Certificate routes — clean rewrite.

GET /certificates            → all certs for the logged-in worker
GET /certificates/{cert_id}  → single cert detail
GET /verify/{cert_id}        → PUBLIC verification endpoint for lenders/banks
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.config.database import get_supabase
from app.routes.auth import get_current_user

router = APIRouter(tags=["certificates"])


def _format_cert(cert: dict) -> dict:
    """Format a certificate row into a clean frontend-friendly shape."""
    issued = cert.get("generated_at", "")
    try:
        dt = datetime.fromisoformat(issued.replace("Z", "+00:00"))
        issued_fmt = dt.strftime("%d %B %Y").lstrip("0")
    except Exception:
        issued_fmt = issued[:10] if issued else None

    return {
        "cert_id": cert.get("cert_id"),
        "version": cert.get("version"),
        "status": cert.get("status"),
        "gigscore": cert.get("gigscore"),
        "gigscore_label": cert.get("gigscore_label"),
        "monthly_avg_inr": cert.get("monthly_avg_inr"),
        "period_start": cert.get("period_start"),
        "period_end": cert.get("period_end"),
        "months_included": cert.get("months_included"),
        "pdf_url": cert.get("pdf_url"),
        "generated_at": issued,
        "issued_formatted": issued_fmt,
    }


@router.get("/certificates")
async def list_certificates(user=Depends(get_current_user)):
    """List all certificates for the authenticated worker, newest first."""
    db = get_supabase()
    result = (
        db.table("certificates")
        .select("*")
        .eq("worker_id", user["id"])
        .order("generated_at", desc=True)
        .execute()
    )
    return {"certificates": [_format_cert(c) for c in (result.data or [])]}


@router.get("/certificates/{cert_id}")
async def get_certificate(cert_id: str, user=Depends(get_current_user)):
    """Get details of a specific certificate owned by the current user."""
    db = get_supabase()
    result = (
        db.table("certificates")
        .select("*")
        .eq("cert_id", cert_id)
        .eq("worker_id", user["id"])
        .execute()
    )
    if not result.data:
        raise HTTPException(404, "Certificate not found.")
    cert = _format_cert(result.data[0])
    cert["worker_name"] = user.get("full_name", "User")
    return cert


@router.get("/verify/{cert_id}")
async def verify_certificate(cert_id: str):
    """
    PUBLIC endpoint — no auth required.
    Banks and lenders use this URL to verify a certificate is genuine.
    """
    db = get_supabase()
    result = (
        db.table("certificates")
        .select("*")
        .eq("cert_id", cert_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(404, {"verified": False, "reason": "Certificate not found."})

    cert = result.data[0]
    worker = db.table("users").select("full_name, city").eq("id", cert["worker_id"]).execute()
    worker_info = worker.data[0] if worker.data else {"full_name": "Unknown", "city": "Unknown"}

    return {
        "verified": cert["status"] == "active",
        "certificate": {
            **_format_cert(cert),
            "worker_name": worker_info["full_name"],
            "worker_city": worker_info["city"],
        }
    }
