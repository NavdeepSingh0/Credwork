import logging
import asyncio
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from app.config.database import get_supabase
from app.routes.auth import get_current_user
from app.models.household import AddWorkerRequest, MakePaymentRequest
from app.utils.razorpay_sim import simulate_razorpay_webhook

router = APIRouter(prefix="/household", tags=["household"])
logger = logging.getLogger(__name__)


def validate_payment_month(payment_month: str, worker_id: str, db) -> bool:
    now = datetime.now()
    current_month = now.strftime('%Y-%m')

    if payment_month == current_month:
        return True  # Current month always allowed

    payment_date = datetime.strptime(payment_month + '-01', '%Y-%m-%d')
    days_ago = (now - payment_date).days

    if days_ago <= 30:
        # Check: max 1 backdated entry per 6-month history
        count_result = db.table("payments").select("id", count="exact") \
            .eq("worker_id", worker_id) \
            .lt("payment_month", current_month) \
            .execute()
        return (count_result.count or 0) < 1

    return False  # More than 30 days — not allowed


@router.get("/dashboard")
async def household_dashboard(user=Depends(get_current_user)):
    if user["role"] != "household":
        raise HTTPException(403, "Only household accounts can access this dashboard.")

    db = get_supabase()

    # Fetch linked active workers with their user details
    workers_result = (
        db.table("household_workers")
        .select("id, worker_id, worker_role, monthly_salary, payment_day, users!worker_id(full_name)")
        .eq("household_id", user["id"])
        .eq("is_active", True)
        .execute()
    )

    current_month = datetime.now().strftime("%Y-%m")

    # For each worker, find their last payment and whether current month is paid
    workers = []
    for hw in (workers_result.data or []):
        worker_id = hw["worker_id"]
        worker_name = (hw.get("users") or {}).get("full_name", "Unknown")

        # Get the most recent payment for this worker
        last_pay_result = (
            db.table("payments")
            .select("amount_inr, created_at, payment_month, status")
            .eq("household_id", user["id"])
            .eq("worker_id", worker_id)
            .eq("status", "processed")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        last_pay = last_pay_result.data[0] if last_pay_result.data else None

        # Format last payment date
        last_payment_fmt = None
        if last_pay and last_pay.get("created_at"):
            try:
                dt = datetime.fromisoformat(last_pay["created_at"].replace("Z", "+00:00"))
                last_payment_fmt = dt.strftime("%d %b %Y").lstrip("0")  # "1 Feb 2025"
            except Exception:
                last_payment_fmt = str(last_pay["created_at"])[:10]

        # Check if current month is already paid
        march_paid_result = (
            db.table("payments")
            .select("id")
            .eq("household_id", user["id"])
            .eq("worker_id", worker_id)
            .eq("payment_month", current_month)
            .filter("status", "in", '("processed","pending")')
            .execute()
        )
        march_paid = bool(march_paid_result.data)

        workers.append({
            "id": str(worker_id),
            "name": worker_name,
            "role": hw.get("worker_role", "Worker"),
            "salary": hw.get("monthly_salary", 0),
            "lastPayment": last_payment_fmt,
            "marchPaid": march_paid,
        })

    return {
        "id": str(user["id"]),
        "name": user["full_name"],
        "city": user.get("city"),
        "role": "household",
        "workers": workers,
    }



@router.post("/add-worker")
async def add_worker(body: AddWorkerRequest, user=Depends(get_current_user)):
    if user["role"] != "household":
        raise HTTPException(403, "Only households can add workers.")

    if body.payment_day < 1 or body.payment_day > 28:
        raise HTTPException(400, "Payment day must be between 1 and 28.")

    db = get_supabase()

    # Look up worker by phone
    worker_result = db.table("users").select("*") \
        .eq("phone", body.worker_phone) \
        .eq("role", "domestic_worker") \
        .execute()

    if worker_result.data:
        worker = worker_result.data[0]

        # Check if already linked
        existing_link = db.table("household_workers").select("id") \
            .eq("household_id", user["id"]) \
            .eq("worker_id", worker["id"]) \
            .execute()

        if existing_link.data:
            raise HTTPException(409, "This worker is already linked to your household.")

        # Create the link
        link = db.table("household_workers").insert({
            "household_id": user["id"],
            "worker_id": worker["id"],
            "worker_role": body.worker_role,
            "monthly_salary": body.monthly_salary,
            "payment_day": body.payment_day,
            "is_active": True
        }).execute()

        return {
            "status": "linked",
            "worker_id": worker["id"],
            "household_worker_id": link.data[0]["id"]
        }
    else:
        # Worker doesn't exist yet — create a placeholder account
        new_worker = db.table("users").insert({
            "phone": body.worker_phone,
            "role": "domestic_worker",
            "full_name": f"Worker ({body.worker_phone})",
            "city": user.get("city", ""),
            "is_verified": False
        }).execute().data[0]

        link = db.table("household_workers").insert({
            "household_id": user["id"],
            "worker_id": new_worker["id"],
            "worker_role": body.worker_role,
            "monthly_salary": body.monthly_salary,
            "payment_day": body.payment_day,
            "is_active": True
        }).execute()

        # STUB: In production, send SMS invite here
        logger.info("[household] SMS invite stub: worker_phone=%s", body.worker_phone)

        return {
            "status": "invited",
            "worker_id": new_worker["id"],
            "household_worker_id": link.data[0]["id"]
        }


@router.get("/workers")
async def get_household_workers(user=Depends(get_current_user)):
    if user["role"] != "household":
        raise HTTPException(403, "Only households can view linked workers.")

    db = get_supabase()
    result = db.table("household_workers") \
        .select("*, users!worker_id(full_name, phone, city, is_verified)") \
        .eq("household_id", user["id"]) \
        .execute()

    return {"workers": result.data}


@router.delete("/workers/{link_id}")
async def remove_worker(link_id: str, user=Depends(get_current_user)):
    if user["role"] != "household":
        raise HTTPException(403, "Only households can remove workers.")

    db = get_supabase()

    # Verify the link belongs to this household
    link = db.table("household_workers").select("*") \
        .eq("id", link_id) \
        .eq("household_id", user["id"]) \
        .execute()

    if not link.data:
        raise HTTPException(404, "Worker link not found.")

    # Soft delete — mark inactive
    db.table("household_workers").update({"is_active": False}) \
        .eq("id", link_id).execute()

    return {"status": "removed", "link_id": link_id}


@router.post("/payment")
async def make_payment(
    body: MakePaymentRequest,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user)
):
    if user["role"] != "household":
        raise HTTPException(403, "Only households can make payments.")

    if body.payment_type not in ["salary", "bonus", "advance"]:
        raise HTTPException(400, "payment_type must be 'salary', 'bonus', or 'advance'.")

    db = get_supabase()

    # Validate link exists and is active
    link = db.table("household_workers").select("*") \
        .eq("household_id", user["id"]) \
        .eq("worker_id", body.worker_id) \
        .eq("is_active", True) \
        .execute()

    if not link.data:
        raise HTTPException(404, "No active link to this worker.")

    # Validate payment month (backdating rules)
    if not validate_payment_month(body.payment_month, body.worker_id, db):
        raise HTTPException(400, "Invalid payment month. Backdating is limited to 1 month and max 1 backdated payment per 6-month window.")

    # Create payment record
    payment = db.table("payments").insert({
        "household_id": user["id"],
        "worker_id": body.worker_id,
        "amount_inr": body.amount_inr,
        "payment_type": body.payment_type,
        "payment_month": body.payment_month,
        "status": "pending"
    }).execute()

    payment_id = payment.data[0]["id"]

    # Fire Razorpay simulation in background (3-second delay)
    background_tasks.add_task(simulate_razorpay_webhook, payment_id)

    return {"payment_id": payment_id, "status": "pending"}


@router.get("/payment-status/{payment_id}")
async def get_payment_status(payment_id: str, user=Depends(get_current_user)):
    if user["role"] != "household":
        raise HTTPException(403, "Only households can check payment status.")

    db = get_supabase()
    result = db.table("payments").select("*") \
        .eq("id", payment_id) \
        .eq("household_id", user["id"]) \
        .execute()

    if not result.data:
        raise HTTPException(404, "Payment not found.")

    return result.data[0]


@router.get("/payments")
async def get_all_payments(user=Depends(get_current_user)):
    if user["role"] != "household":
        raise HTTPException(403, "Only households can view payment history.")

    db = get_supabase()
    result = db.table("payments").select("*") \
        .eq("household_id", user["id"]) \
        .order("created_at", desc=True) \
        .execute()

    return {"payments": result.data}


@router.get("/payments/{worker_id}")
async def get_worker_payments(worker_id: str, user=Depends(get_current_user)):
    if user["role"] != "household":
        raise HTTPException(403, "Only households can view worker payment history.")

    db = get_supabase()
    result = db.table("payments").select("*") \
        .eq("household_id", user["id"]) \
        .eq("worker_id", worker_id) \
        .order("created_at", desc=True) \
        .execute()

    return {"payments": result.data}
