"""
Pydantic models for auth endpoints.
Shapes match the frontend AuthContext.User interface exactly.
"""
from pydantic import BaseModel
from typing import Optional


# ── Request Bodies ──────────────────────────────────────────────

class SendOTPRequest(BaseModel):
    phone: str


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str


class SetupProfileRequest(BaseModel):
    temp_token: str
    role: str  # 'gig_worker' | 'domestic_worker' | 'household'
    full_name: str
    city: str
    photo_url: Optional[str] = None


# ── Response Shapes ────────────────────────────────────────────

class UserResponse(BaseModel):
    """
    Must match frontend AuthContext.User:
    { id, phone, role, full_name, city, photo_url, is_verified }
    """
    id: str
    phone: str
    role: str
    full_name: str
    city: Optional[str] = None
    photo_url: Optional[str] = None
    is_verified: bool = False
