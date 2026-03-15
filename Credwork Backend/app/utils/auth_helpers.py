import hashlib
import random
import string
from datetime import datetime, timedelta
from jose import jwt
from app.config.settings import settings

def generate_otp() -> str:
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def hash_otp(otp: str, phone: str) -> str:
    """Hash OTP with phone as salt — prevents rainbow table attacks."""
    salted = f"{otp}{phone}{settings.jwt_secret}"
    return hashlib.sha256(salted.encode()).hexdigest()

def verify_otp_hash(otp: str, phone: str, stored_hash: str) -> bool:
    return hash_otp(otp, phone) == stored_hash

def create_access_token(user_id: str, role: str, phone: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "phone": phone,
        "exp": datetime.utcnow() + timedelta(days=settings.jwt_expiry_days)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
