from app.config.database import get_supabase


async def resolve_and_save_income(
    worker_id: str,
    by_platform: dict,
    upload_id: str,
    db
) -> list:
    """
    Merges new income data with existing records.
    
    Rules:
    - PDF upload: newer data always wins. Flag if > 15% divergence.
    - Razorpay payouts: always additive, never replace.
    
    Returns list of months that were updated (for worker notification).
    """
    updated_months = []

    for month, platforms in by_platform.items():
        for platform, amount in platforms.items():

            # Check if an entry already exists for this month + platform
            existing = db.table("income_entries").select("*") \
                .eq("worker_id", worker_id) \
                .eq("month", month) \
                .eq("platform", platform) \
                .execute()

            if existing.data:
                old_entry = existing.data[0]
                old_amount = old_entry["amount_inr"]

                # Calculate divergence
                divergence = abs(amount - old_amount) / max(old_amount, 1)

                if divergence > 0.15:
                    # Flag for manual review — but still accept the newer figure
                    db.table("fraud_flags").insert({
                        "worker_id": worker_id,
                        "upload_id": upload_id,
                        "flag_type": "income_divergence",
                        "flag_reason": (
                            f"Month {month} ({platform}): income changed by "
                            f"{round(divergence * 100)}% between two uploads "
                            f"(₹{old_amount:,} → ₹{amount:,})"
                        )
                    }).execute()

                # Always update to newer figure
                db.table("income_entries").update({
                    "amount_inr": amount,
                    "source_ref": upload_id
                }).eq("id", old_entry["id"]).execute()

                updated_months.append(month)

            else:
                # No existing entry — insert fresh
                db.table("income_entries").insert({
                    "worker_id": worker_id,
                    "month": month,
                    "platform": platform,
                    "amount_inr": amount,
                    "source_type": "pdf_upload",
                    "source_ref": upload_id,
                    "household_id": None
                }).execute()

    return updated_months
