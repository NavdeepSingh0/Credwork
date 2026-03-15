# seed.py — run once: python seed.py

from app.config.database import get_supabase
from app.utils.auth_helpers import create_access_token
import time

db = get_supabase()

def clean_db():
    print("Cleaning old demo data...")
    test_phones = ["9999900001", "9999900002", "9999900003"]
    # Get user IDs for these phones
    users_res = db.table("users").select("id").filter("phone", "in", '("9999900001","9999900002","9999900003")').execute()
    user_ids = [u["id"] for u in (users_res.data or [])]
    
    if user_ids:
        # Format for PostgREST: (id1,id2,id3)
        fmt_ids = "(" + ",".join(f'"{uid}"' for uid in user_ids) + ")"
        
        # Delete explicitly hardcoded certificates to prevent unique ID collisions
        db.table("certificates").delete().in_("cert_id", ["CW-2025-00001", "CW-2025-00002"]).execute()
        # Fallback filter version in case in_ doesn't work for certs either
        db.table("certificates").delete().filter("cert_id", "in", '("CW-2025-00001","CW-2025-00002")').execute()
        
        # Delete dependent tables first
        db.table("income_entries").delete().filter("worker_id", "in", fmt_ids).execute()
        db.table("payments").delete().filter("worker_id", "in", fmt_ids).execute()
        db.table("payments").delete().filter("household_id", "in", fmt_ids).execute()
        db.table("certificates").delete().filter("worker_id", "in", fmt_ids).execute()
        db.table("fraud_flags").delete().filter("worker_id", "in", fmt_ids).execute()
        db.table("pdf_uploads").delete().filter("worker_id", "in", fmt_ids).execute()
        db.table("household_workers").delete().filter("worker_id", "in", fmt_ids).execute()
        db.table("household_workers").delete().filter("household_id", "in", fmt_ids).execute()
        # Finally delete users
        db.table("users").delete().filter("id", "in", fmt_ids).execute()
    print("Clean complete.")

clean_db()

# ── Demo Account 1: Gig Worker ────────────────────────────────
print("Seeding Gig Worker (9999900001)...")
gig_user = db.table("users").insert({
    "phone": "9999900001",
    "role": "gig_worker",
    "full_name": "Raju Kumar",
    "city": "Mumbai",
    "language": "hi",
    "is_verified": True
}).execute().data[0]

income_data = [
    ("2024-10", "Swiggy", 11200),
    ("2024-10", "Blinkit", 6000),
    ("2024-11", "Swiggy", 12800),
    ("2024-11", "Zomato", 7000),
    ("2024-12", "Swiggy", 10500),
    ("2024-12", "Rapido", 5000),
    ("2025-01", "Swiggy", 13000),
    ("2025-01", "Zomato", 8000),
    ("2025-02", "Swiggy", 12400),
    ("2025-02", "Blinkit", 6500),
    ("2025-03", "Swiggy", 11600),
    ("2025-03", "Zomato", 7500),
]

for month, platform, amount in income_data:
    db.table("income_entries").insert({
        "worker_id": gig_user["id"],
        "month": month,
        "platform": platform,
        "amount_inr": amount,
        "source_type": "pdf_upload",
        "source_ref": "demo_seed"
    }).execute()

# Generate a certificate for the gig worker
db.table("certificates").insert({
    "cert_id": "CW-2025-00001",
    "worker_id": gig_user["id"],
    "version": 1,
    "status": "active",
    "period_start": "2024-10",
    "period_end": "2025-03",
    "monthly_avg_inr": 18250,
    "gigscore": 780,
    "gigscore_label": "Excellent",
    "months_included": ["2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03"],
    "pdf_url": "https://example.com/dummy.pdf"
}).execute()

print(f"Gig worker token: {create_access_token(gig_user['id'], 'gig_worker', '9999900001')}")

# ── Demo Account 2: Domestic Worker + Household ───────────────
print("Seeding Domestic Worker (9999900002) and Household (9999900003)...")
domestic_user = db.table("users").insert({
    "phone": "9999900002",
    "role": "domestic_worker",
    "full_name": "Priya Devi",
    "city": "New Delhi",
    "language": "hi",
    "is_verified": True
}).execute().data[0]

household_user = db.table("users").insert({
    "phone": "9999900003",
    "role": "household",
    "full_name": "Sharma Household",
    "city": "New Delhi",
    "language": "en",
    "is_verified": True
}).execute().data[0]

db.table("household_workers").insert({
    "household_id": household_user["id"],
    "worker_id": domestic_user["id"],
    "worker_role": "Cook",
    "monthly_salary": 3500,
    "payment_day": 1,
    "is_active": True
}).execute()

domestic_payments = [
    ("2024-10", 3000),
    ("2024-11", 3500),
    ("2024-12", 4000),
    ("2025-01", 3500),
    ("2025-02", 3500),
]

for month, amount in domestic_payments:
    # Income entry
    db.table("income_entries").insert({
        "worker_id": domestic_user["id"],
        "month": month,
        "household_id": household_user["id"],
        "amount_inr": amount,
        "source_type": "razorpay_payout",
        "source_ref": "demo_seed",
        "platform": None
    }).execute()
    
    # Payments entry
    db.table("payments").insert({
        "household_id": household_user["id"],
        "worker_id": domestic_user["id"],
        "amount_inr": amount,
        "payment_type": "salary",
        "payment_month": month,
        "payment_date": month + "-01",
        "status": "processed"
    }).execute()

# Generate a certificate for domestic worker
db.table("certificates").insert({
    "cert_id": "CW-2025-00002",
    "worker_id": domestic_user["id"],
    "version": 1,
    "status": "active",
    "period_start": "2024-10",
    "period_end": "2025-02",
    "monthly_avg_inr": 3500,
    "gigscore": 650,
    "gigscore_label": "Good",
    "months_included": ["2024-10", "2024-11", "2024-12", "2025-01", "2025-02"],
    "pdf_url": "https://example.com/dummy.pdf"
}).execute()

print(f"Domestic worker token: {create_access_token(domestic_user['id'], 'domestic_worker', '9999900002')}")
print(f"Household token: {create_access_token(household_user['id'], 'household', '9999900003')}")
print("Seed complete.")
