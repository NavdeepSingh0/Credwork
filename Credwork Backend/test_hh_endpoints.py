"""
Test household add-worker and payment explicitly.
"""
import requests, json

BASE = "http://127.0.0.1:8000"

# 1. Login household
requests.post(f"{BASE}/auth/send-otp", json={"phone": "9999900003"})
r_hh = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "9999900003", "otp": "123456"})
hh_token = r_hh.json().get("access_token")

# 2. Login domestic worker to get their ID
requests.post(f"{BASE}/auth/send-otp", json={"phone": "9999900002"})
r_dw = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "9999900002", "otp": "123456"})
dw_token = r_dw.json().get("access_token")
me_r = requests.get(f"{BASE}/auth/me", headers={"Authorization": f"Bearer {dw_token}"})
worker_id = me_r.json().get("id")

print(f"Worker ID: {worker_id}")

print("\n--- Testing POST /household/add-worker ---")
r1 = requests.post(
    f"{BASE}/household/add-worker", 
    headers={"Authorization": f"Bearer {hh_token}"},
    json={"worker_phone": "9999900002", "worker_role": "Maid", "monthly_salary": 5000, "payment_day": 1}
)
print("Status:", r1.status_code)
print("Body:", r1.text)

print("\n--- Testing POST /household/payment ---")
r2 = requests.post(
    f"{BASE}/household/payment",
    headers={"Authorization": f"Bearer {hh_token}"},
    json={
        "worker_id": worker_id, 
        "amount_inr": 5000, 
        "payment_type": "salary", 
        "payment_month": "2025-02"
    }
)
print("Status:", r2.status_code)
print("Body:", r2.text)

if r2.status_code == 200:
    payment_id = r2.json().get("payment_id")
    print("\n--- Testing GET /household/payment-status/{payment_id} ---")
    r3 = requests.get(f"{BASE}/household/payment-status/{payment_id}", headers={"Authorization": f"Bearer {hh_token}"})
    print("Status:", r3.status_code)
    print("Body:", r3.text)

print("\nALL DONE")
