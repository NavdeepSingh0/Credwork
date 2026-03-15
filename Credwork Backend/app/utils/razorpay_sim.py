import asyncio
import uuid
from app.config.database import get_supabase
from app.utils.gigscore import calculate_gigscore
from app.utils.cert_generator import generate_certificate


async def simulate_razorpay_webhook(payment_id: str):
    """
    Simulates a Razorpay payout webhook.
    Called as a background task after payment creation.
    The 3-second delay makes the demo feel like a real payment is processing.
    """
    await asyncio.sleep(3)

    db = get_supabase()
    payment_result = db.table("payments").select("*").eq("id", payment_id).execute()

    if not payment_result.data:
        return

    payment = payment_result.data[0]

    if payment["status"] != "pending":
        return  # Already processed — idempotency guard

    fake_payout_id = f"pout_{uuid.uuid4().hex[:16]}"

    # Mark payment as processed
    db.table("payments").update({
        "status": "processed",
        "razorpay_id": fake_payout_id
    }).eq("id", payment_id).execute()

    # Create or update income entry for worker
    existing = db.table("income_entries").select("*") \
        .eq("worker_id", payment["worker_id"]) \
        .eq("month", payment["payment_month"]) \
        .eq("household_id", payment["household_id"]) \
        .execute()

    if existing.data:
        # Payments are additive — stack them (salary + bonus in same month)
        new_amount = existing.data[0]["amount_inr"] + payment["amount_inr"]
        db.table("income_entries").update({
            "amount_inr": new_amount
        }).eq("id", existing.data[0]["id"]).execute()
    else:
        db.table("income_entries").insert({
            "worker_id": payment["worker_id"],
            "month": payment["payment_month"],
            "household_id": payment["household_id"],
            "amount_inr": payment["amount_inr"],
            "source_type": "razorpay_payout",
            "source_ref": fake_payout_id,
            "platform": None
        }).execute()

    # Recalculate GigScore and regenerate certificate if needed
    all_income = db.table("income_entries").select("month, amount_inr") \
        .eq("worker_id", payment["worker_id"]).execute()

    monthly_totals = {}
    for row in all_income.data:
        m = row["month"]
        monthly_totals[m] = monthly_totals.get(m, 0) + row["amount_inr"]

    gigscore_result = calculate_gigscore(monthly_totals)
    await generate_certificate(payment["worker_id"], gigscore_result, db)
