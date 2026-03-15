"""Capture full traceback from household dashboard 500."""
import requests

BASE = "http://127.0.0.1:8000"
requests.post(f"{BASE}/auth/send-otp", json={"phone": "9999900003"})
r = requests.post(f"{BASE}/auth/verify-otp", json={"phone": "9999900003", "otp": "123456"})
token = r.json().get("access_token", "")
r = requests.get(f"{BASE}/household/dashboard", headers={"Authorization": f"Bearer {token}"})
print("Status:", r.status_code)
# Print the full body to capture the traceback
print(r.text)
