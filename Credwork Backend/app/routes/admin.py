from fastapi import APIRouter, HTTPException
from app.config.database import get_supabase

router = APIRouter(prefix="/admin", tags=["admin"])

# NOTE: No auth on admin routes for hackathon demo. Add API key header post-launch.


@router.get("/stats")
async def admin_stats():
    """Platform-wide statistics for the admin dashboard."""
    db = get_supabase()

    users = db.table("users").select("id, role", count="exact").execute()
    uploads = db.table("pdf_uploads").select("id, status", count="exact").execute()
    certs = db.table("certificates").select("id", count="exact").execute()
    payments = db.table("payments").select("id", count="exact").execute()
    flags = db.table("fraud_flags").select("id, status", count="exact").execute()

    # Count by role
    role_counts = {"gig_worker": 0, "domestic_worker": 0, "household": 0}
    for u in (users.data or []):
        if u["role"] in role_counts:
            role_counts[u["role"]] += 1

    # Count uploads by status
    upload_status = {"processing": 0, "passed": 0, "flagged": 0, "failed": 0}
    for up in (uploads.data or []):
        if up["status"] in upload_status:
            upload_status[up["status"]] += 1

    # Count pending fraud flags
    pending_flags = len([f for f in (flags.data or []) if f["status"] == "pending"])

    return {
        "total_users": users.count or 0,
        "users_by_role": role_counts,
        "total_uploads": uploads.count or 0,
        "uploads_by_status": upload_status,
        "total_certificates": certs.count or 0,
        "total_payments": payments.count or 0,
        "pending_fraud_flags": pending_flags
    }


@router.get("/uploads")
async def admin_uploads():
    """List all PDF uploads with worker info."""
    db = get_supabase()
    result = db.table("pdf_uploads") \
        .select("*, users!worker_id(full_name, phone)") \
        .order("created_at", desc=True) \
        .limit(50) \
        .execute()

    return {"uploads": result.data}


@router.get("/fraud-flags")
async def admin_fraud_flags():
    """List all fraud flags for review."""
    db = get_supabase()
    result = db.table("fraud_flags") \
        .select("*, users!worker_id(full_name, phone)") \
        .order("created_at", desc=True) \
        .limit(50) \
        .execute()

    return {"fraud_flags": result.data}


@router.get("/certificates")
async def admin_certificates():
    """List all issued certificates."""
    db = get_supabase()
    result = db.table("certificates") \
        .select("*, users!worker_id(full_name, phone)") \
        .order("generated_at", desc=True) \
        .limit(50) \
        .execute()

    return {"certificates": result.data}


@router.get("/payments")
async def admin_payments():
    """List all ServiConnect payments."""
    db = get_supabase()
    result = db.table("payments") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(50) \
        .execute()

    return {"payments": result.data}


@router.post("/fraud-flags/{flag_id}/review")
async def review_fraud_flag(flag_id: str, action: str, review_note: str = ""):
    """
    Admin reviews a fraud flag.
    action: 'approved' (flag is valid, fraud confirmed) or 'rejected' (false positive)
    """
    if action not in ["approved", "rejected"]:
        raise HTTPException(400, "Action must be 'approved' or 'rejected'.")

    db = get_supabase()

    existing = db.table("fraud_flags").select("*").eq("id", flag_id).execute()
    if not existing.data:
        raise HTTPException(404, "Fraud flag not found.")

    db.table("fraud_flags").update({
        "status": action,
        "reviewed_by": "admin",
        "review_note": review_note
    }).eq("id", flag_id).execute()

    return {
        "status": "reviewed",
        "flag_id": flag_id,
        "action": action
    }
