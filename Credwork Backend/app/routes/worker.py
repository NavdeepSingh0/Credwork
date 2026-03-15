"""
Worker routes — returns data matching the exact frontend DEMO_GIG_WORKER shape.

DEMO_GIG_WORKER expected by frontend:
{
  id, name, city, role, gigscore, gigscoreLabel, monthlyAvgInr,
  certificateId, certificateVersion, certificateStatus, certificateIssued,
  incomeMonths: [{ month, amount, pct }],
  platforms: [...]
}
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.config.database import get_supabase
from app.routes.auth import get_current_user

router = APIRouter(prefix="/worker", tags=["worker"])


def _build_income_months(income_rows: list) -> tuple[list, int, list]:
    """
    Build the incomeMonths array (last 6 months) expected by the frontend,
    and also return monthlyAvgInr and platform list.
    Returns: (incomeMonths, monthlyAvgInr, platforms)
    """
    # Group by month
    monthly: dict[str, int] = {}
    platforms: set[str] = set()

    for row in income_rows:
        month = row["month"]   # "YYYY-MM"
        monthly[month] = monthly.get(month, 0) + row["amount_inr"]
        if row.get("platform"):
            platforms.add(row["platform"])

    if not monthly:
        return [], 0, []

    # Take most recent 6 months, sorted newest → oldest
    sorted_months = sorted(monthly.keys(), reverse=True)[:6]
    amounts = [monthly[m] for m in sorted_months]
    max_amount = max(amounts) if amounts else 1

    income_months = []
    for m in reversed(sorted_months):   # oldest → newest for display
        amt = monthly[m]
        dt = datetime.strptime(m, "%Y-%m")
        income_months.append({
            "month": dt.strftime("%b"),  # "Oct", "Nov" ...
            "amount": amt,
            "pct": round((amt / max_amount) * 100) if max_amount else 0,
        })

    monthly_avg = round(sum(amounts) / len(amounts)) if amounts else 0
    return income_months, monthly_avg, sorted(platforms)


@router.get("/dashboard")
async def get_worker_dashboard(user=Depends(get_current_user)):
    """
    Returns dashboard data matching the frontend DEMO_GIG_WORKER shape exactly.
    """
    if user["role"] not in ("gig_worker", "domestic_worker"):
        raise HTTPException(403, "This route is for workers only.")

    db = get_supabase()

    # Fetch income entries (last 6 months worth)
    income_result = (
        db.table("income_entries")
        .select("month, platform, amount_inr")
        .eq("worker_id", user["id"])
        .order("month", desc=True)
        .limit(200)
        .execute()
    )

    income_months, monthly_avg, platforms = _build_income_months(income_result.data or [])

    # Fetch latest active certificate
    cert_result = (
        db.table("certificates")
        .select("cert_id, version, status, gigscore, gigscore_label, generated_at")
        .eq("worker_id", user["id"])
        .eq("status", "active")
        .order("generated_at", desc=True)
        .limit(1)
        .execute()
    )

    cert = cert_result.data[0] if cert_result.data else None

    # Format certificate issued date
    cert_issued = None
    if cert and cert.get("generated_at"):
        try:
            dt = datetime.fromisoformat(cert["generated_at"].replace("Z", "+00:00"))
            cert_issued = dt.strftime("%d %B %Y").lstrip("0")
        except Exception:
            cert_issued = cert["generated_at"][:10]

    return {
        # Identity — matches DEMO_GIG_WORKER top-level fields
        "id": str(user["id"]),
        "name": user["full_name"],
        "city": user.get("city"),
        "role": user["role"],
        # GigScore
        "gigscore": cert["gigscore"] if cert else 0,
        "gigscoreLabel": cert["gigscore_label"] if cert else "Insufficient",
        # Income
        "monthlyAvgInr": monthly_avg,
        "incomeMonths": income_months,
        "platforms": platforms,
        # Certificate
        "certificateId": cert["cert_id"] if cert else None,
        "certificateVersion": cert["version"] if cert else None,
        "certificateStatus": cert["status"] if cert else "none",
        "certificateIssued": cert_issued,
    }


@router.get("/income")
async def get_worker_income(user=Depends(get_current_user)):
    """Returns full income history for a gig worker."""
    if user["role"] != "gig_worker":
        raise HTTPException(403, "Only gig workers have platform income records.")

    db = get_supabase()
    rows = (
        db.table("income_entries")
        .select("month, platform, amount_inr, source_type")
        .eq("worker_id", user["id"])
        .order("month", desc=True)
        .execute()
    )
    return {"income_history": rows.data or []}
