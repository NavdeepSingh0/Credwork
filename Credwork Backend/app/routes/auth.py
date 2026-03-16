"""
Auth routes — rebuilt to exactly match frontend API contracts.

Endpoints:
  POST /auth/send-otp       → sends OTP (or returns backdoor hint)
  POST /auth/verify-otp     → returns existing_user or new_user
  POST /auth/setup-profile  → creates user, returns access_token + user
  GET  /auth/me             → returns current user from token
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config.database import get_supabase
from app.config.settings import settings
from app.utils.auth_helpers import (
    generate_otp, hash_otp, verify_otp_hash,
    create_access_token, decode_token,
)
from app.utils.sms import send_otp_sms
from app.models.auth import (
    SendOTPRequest, VerifyOTPRequest, SetupProfileRequest, UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer(auto_error=False)


# ── Helpers ────────────────────────────────────────────────────

def _user_to_response(row: dict) -> dict:
    """
    Converts a raw Supabase `users` row into the exact shape
    the frontend AuthContext.User expects.
    """
    return {
        "id": str(row["id"]),
        "phone": row["phone"],
        "role": row["role"],
        "full_name": row.get("full_name"),
        "city": row.get("city"),
        "photo_url": row.get("photo_url"),
        "is_verified": row.get("is_verified", False),
    }


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Dependency that extracts the JWT from the Authorization header,
    decodes it, and returns the full user row from Supabase.
    """
    if not credentials:
        raise HTTPException(401, "Missing authorization header.")

    try:
        payload = decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(401, "Invalid or expired token.")

    user_id = payload.get("user_id")
    if not user_id or user_id == "temp":
        raise HTTPException(401, "Invalid token — not a full user token.")

    db = get_supabase()
    result = db.table("users").select("*").eq("id", user_id).execute()

    if not result.data:
        raise HTTPException(401, "User not found.")

    return result.data[0]


# ── POST /auth/send-otp ───────────────────────────────────────

@router.post("/send-otp")
async def send_otp(body: SendOTPRequest):
    phone = body.phone.strip()

    if len(phone) < 10:
        raise HTTPException(400, "Invalid phone number.")

    db = get_supabase()
    otp = generate_otp()
    otp_hashed = hash_otp(otp, phone)

    # Store OTP session in Supabase.
    # For the hackathon demo, do not fail the request if session persistence
    # is broken in production - the 123456 backdoor can still complete auth.
    session_store_ok = True
    try:
        db.table("otp_sessions").insert({
            "phone": phone,
            "otp_hash": otp_hashed,
            "expires_at": (datetime.utcnow() + timedelta(minutes=1)).isoformat(),
            "verified": False,
        }).execute()
    except Exception as e:
        session_store_ok = False
        print(f"[AUTH] Could not store OTP session for {phone}: {e}")

    # Send OTP via Fast2SMS (production) or deliver in-app (stub mode)
    sms_result = await send_otp_sms(phone, otp)

    response = {
        "message": sms_result.message,
        "expires_in": 60,
        "sms_mode": sms_result.mode,
    }

    # In stub mode (no SMS API configured), return OTP for in-app notification
    # In production with a real SMS key, this field is never included
    if sms_result.mode == "stub":
        response["otp_hint"] = otp

    return response


# ── POST /auth/verify-otp ─────────────────────────────────────

@router.post("/verify-otp")
async def verify_otp(body: VerifyOTPRequest):
    phone = body.phone.strip()
    db = get_supabase()

    # Backdoor OTP for quick testing — skips the wait
    if body.otp == "123456":
        user_result = db.table("users").select("*").eq("phone", phone).execute()

        if user_result.data:
            user = user_result.data[0]
            token = create_access_token(str(user["id"]), user["role"], user["phone"])
            return {
                "status": "existing_user",
                "access_token": token,
                "user": _user_to_response(user),
            }

        temp_token = create_access_token("temp", "temp", phone)
        return {
            "status": "new_user",
            "temp_token": temp_token,
        }

    # Fetch the most recent unverified OTP session for this phone
    result = (
        db.table("otp_sessions")
        .select("*")
        .eq("phone", phone)
        .eq("verified", False)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        raise HTTPException(400, "No active OTP found. Request a new one.")

    session = result.data[0]

    # Check expiry
    if datetime.utcnow().isoformat() > session["expires_at"]:
        raise HTTPException(400, "OTP expired. Request a new one.")

    # Validate — real hash check OR backdoor "123456"
    is_valid = verify_otp_hash(body.otp, phone, session["otp_hash"])

    if not is_valid:
        raise HTTPException(400, "Invalid OTP.")

    # Mark OTP session as verified
    db.table("otp_sessions").update({"verified": True}).eq("id", session["id"]).execute()

    # Check if this phone already has a user account
    user_result = db.table("users").select("*").eq("phone", phone).execute()

    if user_result.data:
        # ── Existing user → return full token + user data ──
        user = user_result.data[0]
        token = create_access_token(str(user["id"]), user["role"], user["phone"])
        return {
            "status": "existing_user",
            "access_token": token,
            "user": _user_to_response(user),
        }
    else:
        # ── New user → return temp token for profile setup ──
        temp_token = create_access_token("temp", "temp", phone)
        return {
            "status": "new_user",
            "temp_token": temp_token,
        }


# ── POST /auth/setup-profile ──────────────────────────────────

@router.post("/setup-profile")
async def setup_profile(body: SetupProfileRequest):
    db = get_supabase()

    # Decode the temp token to recover the phone number
    try:
        payload = decode_token(body.temp_token)
        phone = payload.get("phone")
        if not phone:
            raise ValueError("No phone in token")
    except Exception:
        raise HTTPException(401, "Invalid or expired temp token.")

    # Ensure user doesn't already exist (edge case: double submission)
    existing = db.table("users").select("id").eq("phone", phone).execute()
    if existing.data:
        user = db.table("users").select("*").eq("phone", phone).execute().data[0]
        token = create_access_token(str(user["id"]), user["role"], user["phone"])
        return {"access_token": token, "user": _user_to_response(user)}

    # Validate role
    valid_roles = {"gig_worker", "domestic_worker", "household"}
    if body.role not in valid_roles:
        raise HTTPException(400, f"Invalid role. Must be one of: {', '.join(valid_roles)}")

    # Insert new user using direct HTTP to bypass supabase-py issues
    import httpx
    insert_data = {
        "phone": phone,
        "role": body.role,
        "full_name": body.full_name.strip(),
        "city": body.city.strip(),
        "is_verified": True,
    }

    print(f"[SETUP-PROFILE] Inserting user: {insert_data}")

    headers = {
        "apikey": settings.supabase_service_key,
        "Authorization": f"Bearer {settings.supabase_service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    try:
        resp = httpx.post(
            f"{settings.supabase_url}/rest/v1/users",
            json=insert_data,
            headers=headers,
            timeout=15,
        )
        print(f"[SETUP-PROFILE] Insert response: {resp.status_code} {resp.text}")

        if resp.status_code in (200, 201):
            rows = resp.json()
            if rows:
                user = rows[0] if isinstance(rows, list) else rows
            else:
                raise HTTPException(500, "Insert returned empty.")
        elif resp.status_code == 409:
            # Conflict — user already exists, fetch them
            refetch = db.table("users").select("*").eq("phone", phone).execute()
            if not refetch.data:
                raise HTTPException(500, "Conflict but user not found.")
            user = refetch.data[0]
        else:
            raise HTTPException(500, f"Supabase insert failed: {resp.status_code} {resp.text}")
    except httpx.HTTPError as e:
        raise HTTPException(500, f"HTTP error during insert: {str(e)}")

    token = create_access_token(str(user["id"]), user["role"], user["phone"])

    return {
        "access_token": token,
        "user": _user_to_response(user),
    }


# ── GET /auth/me ──────────────────────────────────────────────

@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return _user_to_response(user)
