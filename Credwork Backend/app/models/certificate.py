from pydantic import BaseModel
from typing import Optional


class CertificateShareRequest(BaseModel):
    recipient_name: Optional[str] = None
    recipient_email: Optional[str] = None
