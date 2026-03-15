"""
test_e2e.py — End-to-end tests for all 3 Credwork user flows.

Tests against a RUNNING server (uvicorn main:app --port 8000).
Uses seeded demo data with backdoor OTP '123456'.

Run:  python test_e2e.py
"""

import httpx
import sys

BASE = "http://127.0.0.1:8000"
OTP = "123456"

PHONES = {
    "gig_worker": "9999900001",
    "domestic_worker": "9999900002",
    "household": "9999900003",
}

results = {"passed": 0, "failed": 0}

def check(label: str, condition: bool, detail: str = ""):
    if condition:
        results["passed"] += 1
        print(f"  ✅ {label}")
    else:
        results["failed"] += 1
        print(f"  ❌ {label}  — {detail}")


def auth_flow(phone: str) -> str | None:
    """Authenticate with OTP backdoor, return access_token or None."""
    r = httpx.post(f"{BASE}/auth/send-otp", json={"phone": phone}, timeout=30)
    if r.status_code != 200:
        print(f"  ❌ send-otp failed: {r.status_code} {r.text}")
        return None

    r = httpx.post(f"{BASE}/auth/verify-otp", json={"phone": phone, "otp": OTP}, timeout=30)
    if r.status_code != 200:
        print(f"  ❌ verify-otp failed: {r.status_code} {r.text}")
        return None

    data = r.json()
    check("verify-otp returns existing_user", data.get("status") == "existing_user",
          f"got status={data.get('status')}")
    token = data.get("access_token")
    check("access_token present", bool(token))
    return token


def headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── Test 1: Gig Worker ────────────────────────────────────────

def test_gig_worker():
    print("\n" + "=" * 55)
    print("TEST 1: Gig Worker  (9999900001 — Raju Kumar)")
    print("=" * 55)

    token = auth_flow(PHONES["gig_worker"])
    if not token:
        return

    # GET /auth/me
    r = httpx.get(f"{BASE}/auth/me", headers=headers(token), timeout=30)
    check("/auth/me returns 200", r.status_code == 200, f"status={r.status_code}")
    if r.status_code == 200:
        me = r.json()
        check("role is gig_worker", me.get("role") == "gig_worker", f"got {me.get('role')}")

    # GET /worker/dashboard
    r = httpx.get(f"{BASE}/worker/dashboard", headers=headers(token), timeout=30)
    check("/worker/dashboard returns 200", r.status_code == 200, f"status={r.status_code}")
    if r.status_code == 200:
        d = r.json()
        check("name is Raju Kumar", d.get("name") == "Raju Kumar", f"got {d.get('name')}")
        check("gigscore > 0", (d.get("gigscore") or 0) > 0, f"got {d.get('gigscore')}")
        check("incomeMonths present", len(d.get("incomeMonths", [])) > 0,
              f"got {len(d.get('incomeMonths', []))} months")
        check("platforms present", len(d.get("platforms", [])) > 0,
              f"got {d.get('platforms')}")
        check("certificateId present", bool(d.get("certificateId")),
              f"got {d.get('certificateId')}")

    # GET /worker/income
    r = httpx.get(f"{BASE}/worker/income", headers=headers(token), timeout=30)
    check("/worker/income returns 200", r.status_code == 200, f"status={r.status_code}")
    if r.status_code == 200:
        inc = r.json()
        rows = inc.get("income_history", [])
        check("income_history has entries", len(rows) > 0, f"got {len(rows)} rows")


# ── Test 2: Household ─────────────────────────────────────────

def test_household():
    print("\n" + "=" * 55)
    print("TEST 2: Household  (9999900003 — Sharma Household)")
    print("=" * 55)

    token = auth_flow(PHONES["household"])
    if not token:
        return

    # GET /household/dashboard
    r = httpx.get(f"{BASE}/household/dashboard", headers=headers(token), timeout=30)
    check("/household/dashboard returns 200", r.status_code == 200, f"status={r.status_code}")
    if r.status_code == 200:
        d = r.json()
        check("name is Sharma Household", d.get("name") == "Sharma Household",
              f"got {d.get('name')}")
        check("role is household", d.get("role") == "household", f"got {d.get('role')}")
        workers = d.get("workers", [])
        check("has linked workers", len(workers) > 0, f"got {len(workers)} workers")
        if workers:
            check("worker name is Priya Devi", workers[0].get("name") == "Priya Devi",
                  f"got {workers[0].get('name')}")
            check("worker role is Cook", workers[0].get("role") == "Cook",
                  f"got {workers[0].get('role')}")


# ── Test 3: Domestic Worker ───────────────────────────────────

def test_domestic_worker():
    print("\n" + "=" * 55)
    print("TEST 3: Domestic Worker  (9999900002 — Priya Devi)")
    print("=" * 55)

    token = auth_flow(PHONES["domestic_worker"])
    if not token:
        return

    # GET /domestic/dashboard
    r = httpx.get(f"{BASE}/domestic/dashboard", headers=headers(token), timeout=30)
    check("/domestic/dashboard returns 200", r.status_code == 200, f"status={r.status_code}")
    if r.status_code == 200:
        d = r.json()
        check("name is Priya Devi", d.get("name") == "Priya Devi",
              f"got {d.get('name')}")
        check("role is domestic_worker", d.get("role") == "domestic_worker",
              f"got {d.get('role')}")
        check("gigscore > 0", (d.get("gigscore") or 0) > 0, f"got {d.get('gigscore')}")
        check("currentHousehold present", bool(d.get("currentHousehold")),
              f"got {d.get('currentHousehold')}")
        check("payments present", len(d.get("payments", [])) > 0,
              f"got {len(d.get('payments', []))} payments")
        check("certificateId present", bool(d.get("certificateId")),
              f"got {d.get('certificateId')}")


# ── Run ───────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("CREDWORK E2E TEST SUITE")
    print(f"Server: {BASE}")
    print("=" * 55)

    # Quick health check
    try:
        r = httpx.get(f"{BASE}/", timeout=5)
        check("Server reachable", r.status_code == 200, f"status={r.status_code}")
    except httpx.ConnectError:
        print("❌ Cannot connect to server. Start it first:")
        print("   uvicorn main:app --reload --port 8000")
        sys.exit(1)

    test_gig_worker()
    test_household()
    test_domestic_worker()

    passed = results["passed"]
    failed = results["failed"]
    print("\n" + "=" * 55)
    print(f"RESULTS:  {passed} passed, {failed} failed, {passed + failed} total")
    print("=" * 55)

    if failed > 0:
        sys.exit(1)
