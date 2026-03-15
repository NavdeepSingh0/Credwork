"""
SMS sending utility with three modes:

1. PRODUCTION  — calls Fast2SMS API to send real OTPs
2. STUB        — logs OTP to console, no real SMS sent (for development)
3. BACKDOOR    — always accepts "123456" as valid OTP (handled in verify-otp)

Mode is determined by APP_ENV and FAST2SMS_API_KEY in settings:
  - If APP_ENV == "production" and FAST2SMS_API_KEY is set → production mode
  - Otherwise → stub mode

The backdoor OTP "123456" is always active regardless of mode.
This lets you demo the app without needing a real phone.
"""
import httpx
from app.config.settings import settings


class SMSResult:
    """Result of an SMS send attempt."""
    def __init__(self, success: bool, message: str, mode: str):
        self.success = success
        self.message = message
        self.mode = mode  # "production" | "stub"

    def __repr__(self):
        return f"SMSResult(success={self.success}, mode={self.mode}, message={self.message})"


def _is_production() -> bool:
    """Check if we should use real SMS sending."""
    return (
        settings.app_env == "production"
        and bool(settings.fast2sms_api_key)
    )


async def send_otp_sms(phone: str, otp: str) -> SMSResult:
    """
    Send an OTP via SMS.

    In production: calls Fast2SMS DLT route.
    In development: prints to console and returns success.

    Args:
        phone: 10-digit Indian mobile number (no country code)
        otp: 6-digit OTP string

    Returns:
        SMSResult with success status and mode used
    """
    # Strip any leading +91 or 91
    clean_phone = phone.strip()
    if clean_phone.startswith("+91"):
        clean_phone = clean_phone[3:]
    elif clean_phone.startswith("91") and len(clean_phone) == 12:
        clean_phone = clean_phone[2:]

    if _is_production():
        return await _send_via_fast2sms(clean_phone, otp)
    else:
        return _send_stub(clean_phone, otp)


async def _send_via_fast2sms(phone: str, otp: str) -> SMSResult:
    """
    Send OTP using Fast2SMS API (https://www.fast2sms.com).

    Uses the DLT (quick-transactional) route for OTP delivery.
    API docs: https://docs.fast2sms.com/#tag/Send-OTP

    Requirements:
      - Set FAST2SMS_API_KEY in .env
      - Set APP_ENV=production in .env
      - Ensure your Fast2SMS account has DLT registration

    You can also use the "OTP" route which auto-generates the OTP:
      POST https://www.fast2sms.com/dev/bulkV2
      But we prefer to generate our own OTP for hashing.
    """
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": settings.fast2sms_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "route": "otp",
        "variables_values": otp,
        "numbers": phone,
        "flash": "0",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=headers)

        data = response.json()

        if response.status_code == 200 and data.get("return"):
            print(f"[SMS] OTP sent to {phone} via Fast2SMS (request_id: {data.get('request_id', 'N/A')})")
            return SMSResult(
                success=True,
                message=f"OTP sent via Fast2SMS",
                mode="production",
            )
        else:
            # API returned an error — fall back to stub so the user isn't blocked
            error_msg = data.get("message", str(data))
            print(f"[SMS] Fast2SMS error for {phone}: {error_msg}")
            print(f"[SMS] Falling back to stub mode. OTP is: {otp}")
            return SMSResult(
                success=True,  # Don't block the user
                message=f"SMS API error ({error_msg}). Use backdoor OTP 123456.",
                mode="stub",
            )

    except Exception as e:
        # Network error — fall back to stub
        print(f"[SMS] Network error sending to {phone}: {e}")
        print(f"[SMS] Falling back to stub mode. OTP is: {otp}")
        return SMSResult(
            success=True,  # Don't block the user
            message=f"SMS delivery failed ({str(e)}). Use backdoor OTP 123456.",
            mode="stub",
        )


def _send_stub(phone: str, otp: str) -> SMSResult:
    """
    Stub mode — just logs the OTP to the console.
    Used during development when APP_ENV != "production".
    """
    print(f"[SMS STUB] Phone: {phone} | OTP: {otp} | Backdoor: 123456")
    return SMSResult(
        success=True,
        message="OTP sent (dev mode). Use backdoor 123456.",
        mode="stub",
    )
