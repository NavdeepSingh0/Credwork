"""
Directly test the household dashboard logic via the HTTP endpoint with debug.
Checks if get_current_user works for household role.
"""
import requests, json

BASE = "http://127.0.0.1:8000"

# Step 1: send otp
requests.post(f"{BASE}/auth/send-otp", json={"phone": "9999900003"})

# Step 2: verify otp
r = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "9999900003", "otp": "123456"})
print("verify-otp status:", r.status_code)
d = r.json()
print("verify-otp body:", json.dumps(d, indent=2))
token = d.get("access_token", "")

# Step 3: /auth/me (checking get_current_user works for household)
r = requests.get(f"{BASE}/auth/me", headers={"Authorization": f"Bearer {token}"})
print()
print("/auth/me status:", r.status_code)
print("/auth/me body:", r.text[:400])

# Step 4: try household dashboard
r = requests.get(f"{BASE}/household/dashboard", headers={"Authorization": f"Bearer {token}"})
print()
print("/household/dashboard status:", r.status_code)
print("/household/dashboard body:", r.text[:2000])
