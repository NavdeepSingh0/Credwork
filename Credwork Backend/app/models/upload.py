from pydantic import BaseModel
from typing import Optional, List


class UploadResponse(BaseModel):
    status: str
    upload_id: str
    months_found: Optional[int] = None
    platforms_found: Optional[List[str]] = None
    monthly_avg: Optional[int] = None
    gigscore: Optional[int] = None
    gigscore_label: Optional[str] = None
    fraud_checklist: Optional[dict] = None
    certificate_id: Optional[str] = None
