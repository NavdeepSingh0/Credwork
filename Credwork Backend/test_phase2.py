"""Test Phase 2 endpoints — worker dashboard and certificates."""
import requests
import json

BASE = "http://127.0.0.1:8000"

# Get auth token for gig worker
requests.post(f"{BASE}/auth/send-otp", json={"phone": "9999900001"})
r = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "9999900001", "otp": "123456"})
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

print("=== GET /worker/dashboard (gig worker 9999900001) ===")
r = requests.get(f"{BASE}/worker/dashboard", headers=headers)
print(f"Status: {r.status_code}")
d = r.json()
print(f"  Keys: {sorted(d.keys())}")
print(f"  name: {d.get('name')}")
print(f"  role: {d.get('role')}")
print(f"  gigscore: {d.get('gigscore')}")
print(f"  gigscoreLabel: {d.get('gigscoreLabel')}")
print(f"  monthlyAvgInr: {d.get('monthlyAvgInr')}")
print(f"  certificateId: {d.get('certificateId')}")
print(f"  platforms: {d.get('platforms')}")
print(f"  incomeMonths count: {len(d.get('incomeMonths', []))}")

print()
print("=== GET /worker/income ===")
r = requests.get(f"{BASE}/worker/income", headers=headers)
print(f"Status: {r.status_code}")
d = r.json()
print(f"  income_history count: {len(d.get('income_history', []))}")

print()
print("=== GET /certificates ===")
r = requests.get(f"{BASE}/certificates", headers=headers)
print(f"Status: {r.status_code}")
d = r.json()
certs = d.get("certificates", [])
print(f"  Certificates count: {len(certs)}")
if certs:
    print(f"  First cert keys: {sorted(certs[0].keys())}")
    print(f"  First cert: cert_id={certs[0].get('cert_id')}, status={certs[0].get('status')}")

print()
print("ALL TESTS DONE")
