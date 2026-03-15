from fastapi import APIRouter, HTTPException, Depends
from app.config.database import get_supabase
from app.routes.auth import get_current_user

router = APIRouter(prefix="/settings", tags=["settings"])


@router.put("/language")
async def update_language(language: str, user=Depends(get_current_user)):
    """Update user's preferred language."""
    if language not in ["en", "hi"]:
        raise HTTPException(400, "Language must be 'en' or 'hi'.")

    db = get_supabase()
    db.table("users").update({"language": language}).eq("id", user["id"]).execute()

    return {"status": "updated", "language": language}


@router.put("/notifications")
async def update_notifications(enabled: bool = True, user=Depends(get_current_user)):
    """
    STUB: Toggle notification preferences.
    In production, this would update a notifications_enabled column.
    For demo, we just acknowledge the toggle.
    """
    print(f"🔔 STUB: Notifications {'enabled' if enabled else 'disabled'} for user {user['id']}")
    return {"status": "updated", "notifications_enabled": enabled}


@router.get("/data-export")
async def export_user_data(user=Depends(get_current_user)):
    """
    DPDP compliance: Export all user data as JSON.
    Returns all records associated with this user.
    """
    db = get_supabase()

    user_data = db.table("users").select("*").eq("id", user["id"]).execute()

    income = db.table("income_entries").select("*") \
        .eq("worker_id", user["id"]).execute()

    certificates = db.table("certificates").select("*") \
        .eq("worker_id", user["id"]).execute()

    uploads = db.table("pdf_uploads").select("*") \
        .eq("worker_id", user["id"]).execute()

    payments_made = db.table("payments").select("*") \
        .eq("household_id", user["id"]).execute()

    payments_received = db.table("payments").select("*") \
        .eq("worker_id", user["id"]).execute()

    return {
        "user": user_data.data[0] if user_data.data else None,
        "income_entries": income.data,
        "certificates": certificates.data,
        "pdf_uploads": uploads.data,
        "payments_made": payments_made.data,
        "payments_received": payments_received.data
    }
