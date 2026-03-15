"""Test Phase 3 endpoints — household dashboard and domestic worker dashboard."""
import requests
import json

BASE = "http://127.0.0.1:8000"


def get_token(phone):
    requests.post(f"{BASE}/auth/send-otp", json={"phone": phone})
    r = requests.post(f"{BASE}/auth/verify-otp", json={"phone": phone, "otp": "123456"})
    return r.json().get("access_token")


# === HOUSEHOLD DASHBOARD ===
print("=== GET /household/dashboard (9999900003) ===")
token = get_token("9999900003")
r = requests.get(f"{BASE}/household/dashboard", headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
d = r.json()
print(f"  Top-level keys: {sorted(d.keys())}")
print(f"  id: {d.get('id')}")
print(f"  name: {d.get('name')}")
print(f"  city: {d.get('city')}")
print(f"  role: {d.get('role')}")
workers = d.get("workers", [])
print(f"  workers count: {len(workers)}")
for w in workers:
    print(f"    -> name={w.get('name')} role={w.get('role')} salary={w.get('salary')} marchPaid={w.get('marchPaid')}")

print()

# === DOMESTIC WORKER DASHBOARD ===
print("=== GET /domestic/dashboard (9999900002) ===")
token = get_token("9999900002")
r = requests.get(f"{BASE}/domestic/dashboard", headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
d = r.json()
print(f"  Top-level keys: {sorted(d.keys())}")
print(f"  name: {d.get('name')}")
print(f"  role: {d.get('role')}")
print(f"  currentHousehold: {d.get('currentHousehold')}")
print(f"  householdCity: {d.get('householdCity')}")
print(f"  memberSince: {d.get('memberSince')}")
print(f"  marchPaid: {d.get('marchPaid')}")
print(f"  gigscore: {d.get('gigscore')}")
payments = d.get("payments", [])
print(f"  payments count: {len(payments)}")
if payments:
    print(f"  first payment: {payments[0]}")

print()
print("ALL TESTS DONE")
