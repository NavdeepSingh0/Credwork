"""
Domestic worker routes — returns data matching DEMO_DOMESTIC_WORKER shape exactly.

DEMO_DOMESTIC_WORKER expected by frontend:
{
  id, name, city, role, gigscore, gigscoreLabel, monthlyAvgInr,
  certificateId, certificateVersion, certificateStatus, certificateIssued,
  currentHousehold, householdCity, memberSince, marchPaid,
  payments: [{ month, household, type, date, amount }]
}
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.config.database import get_supabase
from app.routes.auth import get_current_user

router = APIRouter(prefix="/domestic", tags=["domestic"])


@router.get("/dashboard")
async def get_domestic_dashboard(user=Depends(get_current_user)):
    """
    Returns domestic worker dashboard matching DEMO_DOMESTIC_WORKER shape.
    """
    if user["role"] != "domestic_worker":
        raise HTTPException(403, "This route is for domestic workers only.")

    db = get_supabase()
    current_month = datetime.now().strftime("%Y-%m")

    # ── Fetch current household link ──────────────────────────────
    link_result = (
        db.table("household_workers")
        .select("worker_role, monthly_salary, users!household_id(full_name, city)")
        .eq("worker_id", user["id"])
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    link = link_result.data[0] if link_result.data else None
    household_name = None
    household_city = None
    member_since = None

    if link:
        household_info = link.get("users") or {}
        household_name = household_info.get("full_name")
        household_city = household_info.get("city")
        member_since = "Unknown"  # No created_at in the DB for household_workers

    # ── Fetch latest active certificate ───────────────────────────
    cert_result = (
        db.table("certificates")
        .select("cert_id, version, status, gigscore, gigscore_label, monthly_avg_inr, generated_at")
        .eq("worker_id", user["id"])
        .eq("status", "active")
        .order("generated_at", desc=True)
        .limit(1)
        .execute()
    )
    cert = cert_result.data[0] if cert_result.data else None

    cert_issued = None
    if cert and cert.get("generated_at"):
        try:
            dt = datetime.fromisoformat(cert["generated_at"].replace("Z", "+00:00"))
            cert_issued = dt.strftime("%d %B %Y").lstrip("0")
        except Exception:
            cert_issued = cert["generated_at"][:10]

    # ── Check if current month is paid ────────────────────────────
    march_paid_result = (
        db.table("payments")
        .select("id")
        .eq("worker_id", user["id"])
        .eq("payment_month", current_month)
        .filter("status", "in", '("processed","pending")')
        .execute()
    )
    march_paid = bool(march_paid_result.data)

    # ── Fetch payment history ─────────────────────────────────────
    # Note: we don't join users here — payments.household_id has no PostgREST hint
    # We use the household_name already fetched from household_workers above
    payments_result = (
        db.table("payments")
        .select("amount_inr, payment_type, payment_month, created_at, status, household_id")
        .eq("worker_id", user["id"])
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )

    payments = []
    for p in (payments_result.data or []):
        # Format month: "Feb 2025"
        month_fmt = None
        date_fmt = None
        if p.get("payment_month"):
            try:
                dt = datetime.strptime(p["payment_month"], "%Y-%m")
                month_fmt = dt.strftime("%b %Y")
            except Exception:
                month_fmt = p["payment_month"]

        if p.get("created_at"):
            try:
                dt = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
                date_fmt = dt.strftime("%d %b %Y").lstrip("0")
            except Exception:
                date_fmt = str(p["created_at"])[:10]

        payments.append({
            "month": month_fmt,
            "household": household_name or "Unknown",  # from the link query above
            "type": (p.get("payment_type") or "salary").capitalize(),
            "date": date_fmt,
            "amount": p.get("amount_inr", 0),
        })

    # ── Monthly avg from income entries ───────────────────────────
    monthly_avg = cert["monthly_avg_inr"] if cert else (
        link["monthly_salary"] if link else 0
    )

    return {
        # Identity
        "id": str(user["id"]),
        "name": user["full_name"],
        "city": user.get("city"),
        "role": "domestic_worker",
        # GigScore
        "gigscore": cert["gigscore"] if cert else 0,
        "gigscoreLabel": cert["gigscore_label"] if cert else "Insufficient",
        "monthlyAvgInr": monthly_avg,
        # Certificate
        "certificateId": cert["cert_id"] if cert else None,
        "certificateVersion": cert["version"] if cert else None,
        "certificateStatus": cert["status"] if cert else "none",
        "certificateIssued": cert_issued,
        # Household
        "currentHousehold": household_name,
        "householdCity": household_city,
        "memberSince": member_since,
        # Payment status
        "marchPaid": march_paid,
        "payments": payments,
    }
