"""Quick test for Phase 1 auth endpoints."""
import requests
import json

BASE = "http://127.0.0.1:8000"

print("=== 1. SEND OTP ===")
r = requests.post(f"{BASE}/auth/send-otp", json={"phone": "9999900001"})
print(f"Status: {r.status_code}  Body: {r.json()}")

print()
print("=== 2. VERIFY OTP (existing gig worker) ===")
r = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "9999900001", "otp": "123456"})
print(f"Status: {r.status_code}")
d = r.json()
print(f"  status: {d.get('status')}")
if d.get("user"):
    print(f"  user keys: {sorted(d['user'].keys())}")
    print(f"  user: {json.dumps(d['user'], indent=2)}")
token_gig = d.get("access_token", "")

print()
print("=== 3. VERIFY OTP (existing household) ===")
requests.post(f"{BASE}/auth/send-otp", json={"phone": "9999900003"})
r = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "9999900003", "otp": "123456"})
print(f"Status: {r.status_code}")
d = r.json()
print(f"  status: {d.get('status')}")
if d.get("user"):
    print(f"  role: {d['user']['role']}")
    print(f"  name: {d['user']['full_name']}")

print()
print("=== 4. VERIFY OTP (new user) ===")
requests.post(f"{BASE}/auth/send-otp", json={"phone": "5555500099"})
r = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "5555500099", "otp": "123456"})
print(f"Status: {r.status_code}")
d = r.json()
print(f"  status: {d.get('status')}  has_temp_token: {'temp_token' in d}")

print()
print("=== 5. GET /auth/me ===")
if token_gig:
    r = requests.get(f"{BASE}/auth/me", headers={"Authorization": f"Bearer {token_gig}"})
    print(f"Status: {r.status_code}")
    print(f"  Body: {json.dumps(r.json(), indent=2)}")

print()
print("ALL TESTS DONE")
