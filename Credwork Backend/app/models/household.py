from pydantic import BaseModel
from typing import Optional


class AddWorkerRequest(BaseModel):
    worker_phone: str
    worker_role: str
    monthly_salary: int
    payment_day: int


class MakePaymentRequest(BaseModel):
    worker_id: str
    amount_inr: int
    payment_type: str  # "salary", "bonus", "advance"
    payment_month: str  # "YYYY-MM"
