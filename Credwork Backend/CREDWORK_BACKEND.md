# Credwork — Backend Engineering Bible
**Version 1.0 | Hackathon Deadline: 16 March 2025 | Stack: FastAPI + Supabase (PostgreSQL)**

---

## Before You Touch Any Code

Read this document top to bottom once before starting. Every section builds on the previous one. The order matters.

**What we're building:** A FastAPI backend on Vercel that lets gig workers upload bank statements, extracts their UPI income using VPA matching, calculates a GigScore, and generates a bank-ready PDF income certificate. Domestic workers get the same certificate through ServiConnect — a Razorpay-powered payment rail.

**The three things judges will test live:**
1. Upload a fake PDF → fraud detection must reject it
2. Upload a real bank statement → GigScore + certificate must generate
3. Household pays a domestic worker → certificate must update in real time

Everything else can be stubbed. These three cannot.

---

## Table of Contents

1. [Tech Stack & Setup](#1-tech-stack--setup)
2. [Project Structure](#2-project-structure)
3. [Database Schema](#3-database-schema)
4. [Supabase Setup](#4-supabase-setup)
5. [Authentication — OTP Flow](#5-authentication--otp-flow)
6. [PDF Upload Pipeline](#6-pdf-upload-pipeline)
7. [Fraud Stack](#7-fraud-stack)
8. [VPA Extraction & Monthly Aggregation](#8-vpa-extraction--monthly-aggregation)
9. [GigScore Algorithm](#9-gigscore-algorithm)
10. [Conflict Resolution](#10-conflict-resolution)
11. [Certificate Generation](#11-certificate-generation)
12. [ServiConnect — Household Payment Flow](#12-serviconnect--household-payment-flow)
13. [Razorpay Simulation](#13-razorpay-simulation)
14. [All API Endpoints](#14-all-api-endpoints)
15. [VPA Config](#15-vpa-config)
16. [Vercel Deployment](#16-vercel-deployment)
17. [Demo Seed Data](#17-demo-seed-data)
18. [What to Stub vs What Must Be Real](#18-what-to-stub-vs-what-must-be-real)

---

## 1. Tech Stack & Setup

### Stack
| Layer | Choice | Reason |
|---|---|---|
| Runtime | Python 3.11 + FastAPI | Team is fastest here |
| Database | Supabase (PostgreSQL) | Free tier, visual dashboard, Vercel-native |
| PDF parsing | pdfplumber + pikepdf | pdfplumber for extraction, pikepdf for fraud |
| OCR fallback | pytesseract | For scanned/image PDFs |
| Certificate PDF | reportlab | Python-native, no browser needed |
| OTP | Stub (console print) | Real SMS post-hackathon |
| File storage | Local `/certificates` folder | No S3 needed for demo |
| Deployment | Vercel serverless | One command deploy |

### Install everything

```bash
pip install fastapi uvicorn python-multipart pymupdf pikepdf pdfplumber \
  pytesseract Pillow reportlab supabase python-dotenv pydantic \
  pydantic-settings python-jose passlib pandas
```

### Environment variables

Create `.env` in project root:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# Auth
JWT_SECRET=change-this-to-something-random-in-prod
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=30

# App
APP_ENV=development
DEBUG=true
```

---

## 2. Project Structure

```
credwork/
├── main.py                         # FastAPI app entry point
├── requirements.txt
├── vercel.json
├── .env
│
├── app/
│   ├── config/
│   │   ├── settings.py             # Pydantic settings from .env
│   │   ├── database.py             # Supabase client singleton
│   │   └── vpa_config.json         # Known gig platform VPAs
│   │
│   ├── models/
│   │   ├── auth.py                 # Request/response schemas
│   │   ├── upload.py
│   │   ├── certificate.py
│   │   └── household.py
│   │
│   ├── routes/
│   │   ├── auth.py                 # /auth/*
│   │   ├── upload.py               # /upload/*
│   │   ├── worker.py               # /worker/*
│   │   ├── certificates.py         # /certificates/* + /verify/*
│   │   ├── household.py            # /household/*
│   │   ├── settings.py             # /settings/*
│   │   └── admin.py                # /admin/*
│   │
│   └── utils/
│       ├── fraud.py                # PDF fraud detection
│       ├── vpa_parser.py           # VPA extraction + monthly aggregation
│       ├── gigscore.py             # GigScore algorithm
│       ├── cert_generator.py       # ReportLab PDF generation
│       ├── conflict_resolver.py    # Income conflict resolution
│       └── auth_helpers.py        # JWT encode/decode, OTP hash
│
├── certificates/                   # Generated PDFs stored here (local for demo)
└── temp_uploads/                   # Temp storage for PDFs during processing (deleted after)
```

---

## 3. Database Schema

Run this SQL in Supabase's SQL editor in this exact order (foreign keys require the referenced tables to exist first).

```sql
-- ============================================================
-- TABLE: users
-- ============================================================
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  phone           VARCHAR(10) UNIQUE NOT NULL,
  role            VARCHAR(20) NOT NULL 
                  CHECK (role IN ('gig_worker', 'domestic_worker', 'household')),
  full_name       VARCHAR(255),
  city            VARCHAR(100),
  photo_url       VARCHAR(500),
  language        VARCHAR(10) DEFAULT 'en' 
                  CHECK (language IN ('en', 'hi')),
  is_verified     BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLE: otp_sessions
-- ============================================================
CREATE TABLE otp_sessions (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  phone           VARCHAR(10) NOT NULL,
  otp_hash        VARCHAR(255) NOT NULL,
  expires_at      TIMESTAMPTZ NOT NULL,
  verified        BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-cleanup index: speeds up expired OTP queries
CREATE INDEX idx_otp_phone_expiry ON otp_sessions(phone, expires_at);

-- ============================================================
-- TABLE: pdf_uploads
-- ============================================================
CREATE TABLE pdf_uploads (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  worker_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status          VARCHAR(20) NOT NULL DEFAULT 'processing'
                  CHECK (status IN ('processing', 'passed', 'flagged', 'failed')),
  fraud_check     VARCHAR(20) CHECK (fraud_check IN ('passed', 'flagged', 'failed')),
  fraud_reason    TEXT,
  months_found    INTEGER,
  platforms_found TEXT[],
  processed_at    TIMESTAMPTZ,
  created_at      TIMESTAMPTZ DEFAULT NOW()
  -- IMPORTANT: The actual PDF file is NEVER stored in the database.
  -- It is processed in memory and deleted immediately after parsing.
);

-- ============================================================
-- TABLE: income_entries
-- ============================================================
CREATE TABLE income_entries (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  worker_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  month           VARCHAR(7) NOT NULL,       -- Format: YYYY-MM e.g. "2025-01"
  platform        VARCHAR(100),              -- "Swiggy", "Zomato" etc. NULL for domestic workers
  household_id    UUID REFERENCES users(id), -- NULL for gig workers
  amount_inr      INTEGER NOT NULL,          -- Always store in whole rupees
  source_type     VARCHAR(20) NOT NULL 
                  CHECK (source_type IN ('pdf_upload', 'razorpay_payout')),
  source_ref      VARCHAR(255),              -- upload_id or Razorpay payout ID
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(worker_id, month, platform, household_id)  -- Prevents duplicate entries
);

CREATE INDEX idx_income_worker_month ON income_entries(worker_id, month);

-- ============================================================
-- TABLE: certificates
-- ============================================================
CREATE TABLE certificates (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cert_id         VARCHAR(20) UNIQUE NOT NULL, -- Format: CW-2025-00847
  worker_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  version         INTEGER NOT NULL DEFAULT 1,
  status          VARCHAR(20) NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active', 'superseded')),
  period_start    VARCHAR(7) NOT NULL,         -- YYYY-MM
  period_end      VARCHAR(7) NOT NULL,         -- YYYY-MM
  monthly_avg_inr INTEGER NOT NULL,
  gigscore        INTEGER NOT NULL,            -- 0–100
  gigscore_label  VARCHAR(20) NOT NULL,        -- Excellent / Good / Moderate / Low / Insufficient
  months_included JSONB NOT NULL,              -- [{month, amount, platform}]
  pdf_url         VARCHAR(500) NOT NULL,       -- Permanent, immutable URL
  generated_at    TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(worker_id, version)
);

-- ============================================================
-- TABLE: household_workers (linking table)
-- ============================================================
CREATE TABLE household_workers (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  worker_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  worker_role     VARCHAR(100) NOT NULL,       -- "Cook", "Driver", "Cleaner" etc.
  monthly_salary  INTEGER NOT NULL,
  payment_day     INTEGER NOT NULL CHECK (payment_day BETWEEN 1 AND 28),
  linked_at       TIMESTAMPTZ DEFAULT NOW(),
  is_active       BOOLEAN DEFAULT TRUE,
  UNIQUE(household_id, worker_id)
);

-- ============================================================
-- TABLE: payments (ServiConnect)
-- ============================================================
CREATE TABLE payments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  worker_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount_inr      INTEGER NOT NULL,
  payment_type    VARCHAR(20) NOT NULL 
                  CHECK (payment_type IN ('salary', 'bonus', 'advance')),
  payment_month   VARCHAR(7) NOT NULL,         -- YYYY-MM
  payment_date    DATE NOT NULL,
  razorpay_ref    VARCHAR(255),
  status          VARCHAR(20) NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'processed', 'failed')),
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLE: fraud_flags (admin review queue)
-- ============================================================
CREATE TABLE fraud_flags (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  worker_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  upload_id       UUID REFERENCES pdf_uploads(id),
  flag_type       VARCHAR(50) NOT NULL,
  flag_reason     TEXT NOT NULL,
  status          VARCHAR(20) DEFAULT 'pending'
                  CHECK (status IN ('pending', 'approved', 'rejected')),
  reviewed_by     VARCHAR(100),
  review_note     TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- SEQUENCE: Certificate ID counter
-- ============================================================
CREATE SEQUENCE cert_sequence START 1;
```

---

## 4. Supabase Setup

1. Go to [supabase.com](https://supabase.com) → New project
2. Copy your **Project URL** and **service_role key** (not anon key — service role bypasses RLS for backend operations) into `.env`
3. Open SQL Editor → paste and run the entire schema above
4. Verify tables created: Table Editor should show 7 tables

**Row Level Security:** Disable RLS for all tables during the hackathon. You're using the service role key server-side, so RLS is irrelevant. Add it post-launch.

```sql
-- Run this to disable RLS on all tables for hackathon speed
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE otp_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE pdf_uploads DISABLE ROW LEVEL SECURITY;
ALTER TABLE income_entries DISABLE ROW LEVEL SECURITY;
ALTER TABLE certificates DISABLE ROW LEVEL SECURITY;
ALTER TABLE household_workers DISABLE ROW LEVEL SECURITY;
ALTER TABLE payments DISABLE ROW LEVEL SECURITY;
ALTER TABLE fraud_flags DISABLE ROW LEVEL SECURITY;
```

---

## 5. Authentication — OTP Flow

### Flow

```
User enters phone
      ↓
POST /auth/send-otp
  → Generate 6-digit OTP
  → Hash with SHA-256 + salt
  → Store in otp_sessions (5-min expiry)
  → [STUB] Print to console: "OTP for 9876543210: 482910"
      ↓
User enters OTP
      ↓
POST /auth/verify-otp
  → Check hash matches
  → Check not expired
  → New user  → return { status: "new_user", temp_token }
  → Existing  → return { status: "existing_user", access_token, user }
      ↓
If new user:
POST /auth/setup-profile
  → Create user record
  → Return access_token
```

### Code: `app/utils/auth_helpers.py`

```python
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
```

### Code: `app/routes/auth.py`

```python
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from app.config.database import get_supabase
from app.utils.auth_helpers import (
    generate_otp, hash_otp, verify_otp_hash, create_access_token, decode_token
)
from app.models.auth import (
    SendOTPRequest, VerifyOTPRequest, SetupProfileRequest
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/send-otp")
async def send_otp(body: SendOTPRequest):
    db = get_supabase()
    otp = generate_otp()
    otp_hash = hash_otp(otp, body.phone)
    expires_at = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

    db.table("otp_sessions").insert({
        "phone": body.phone,
        "otp_hash": otp_hash,
        "expires_at": expires_at,
        "verified": False
    }).execute()

    # STUB: Print to console instead of sending SMS
    print(f"\n{'='*40}")
    print(f"OTP for {body.phone}: {otp}")
    print(f"{'='*40}\n")

    return {"message": "OTP sent", "expires_in": 300}


@router.post("/verify-otp")
async def verify_otp(body: VerifyOTPRequest):
    db = get_supabase()

    # Get the most recent unverified OTP for this phone
    result = db.table("otp_sessions") \
        .select("*") \
        .eq("phone", body.phone) \
        .eq("verified", False) \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()

    if not result.data:
        raise HTTPException(400, "No active OTP found. Request a new one.")

    session = result.data[0]

    # Check expiry
    if datetime.utcnow().isoformat() > session["expires_at"]:
        raise HTTPException(400, "OTP expired. Request a new one.")

    # Check hash — also allow "123456" for demo phones
    is_demo_otp = body.otp == "123456"
    is_valid_otp = verify_otp_hash(body.otp, body.phone, session["otp_hash"])

    if not (is_valid_otp or is_demo_otp):
        raise HTTPException(400, "Invalid OTP.")

    # Mark session as verified
    db.table("otp_sessions").update({"verified": True}) \
        .eq("id", session["id"]).execute()

    # Check if user exists
    user_result = db.table("users").select("*").eq("phone", body.phone).execute()

    if user_result.data:
        user = user_result.data[0]
        token = create_access_token(user["id"], user["role"], user["phone"])
        return {"status": "existing_user", "access_token": token, "user": user}
    else:
        # New user — return temp token for profile setup
        temp_token = create_access_token("temp", "temp", body.phone)
        return {"status": "new_user", "temp_token": temp_token}


@router.post("/setup-profile")
async def setup_profile(body: SetupProfileRequest):
    db = get_supabase()

    # Decode temp token to get phone
    try:
        payload = decode_token(body.temp_token)
        phone = payload["phone"]
    except Exception:
        raise HTTPException(401, "Invalid or expired token.")

    # Create user
    user_data = {
        "phone": phone,
        "role": body.role,
        "full_name": body.full_name,
        "city": body.city,
        "photo_url": body.photo_url,
        "language": body.language,
        "is_verified": True
    }

    result = db.table("users").insert(user_data).execute()
    user = result.data[0]
    token = create_access_token(user["id"], user["role"], user["phone"])

    return {"access_token": token, "user": user}


@router.get("/me")
async def get_me(token: str = Depends(lambda x: x)):
    # Implement Bearer token extraction via FastAPI dependency
    pass
```

---

## 6. PDF Upload Pipeline

The most critical part of the backend. Do not reorder these steps.

```
Receive PDF
    ↓
Step 1: Validate (MIME type, size, role)
    ↓
Step 2: Save to temp_uploads/ + create pdf_uploads record (status: processing)
    ↓
Step 3: Run fraud stack (pikepdf)
    → FAIL: Delete file, update record (status: failed), return error, STOP
    → PASS: Continue
    ↓
Step 4: Extract gig transactions (pdfplumber + VPA matching)
    ↓
Step 5: Aggregate by month
    ↓
Step 6: Resolve conflicts with existing income records
    ↓
Step 7: Save income_entries to database
    ↓
Step 8: Delete PDF from temp storage
    ↓
Step 9: Calculate GigScore
    ↓
Step 10: Generate certificate if threshold met (3+ months)
    ↓
Step 11: Update pdf_uploads record (status: passed)
    ↓
Return result
```

### Code: `app/routes/upload.py`

```python
import os
import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.config.database import get_supabase
from app.utils.fraud import run_fraud_checks
from app.utils.vpa_parser import extract_gig_income, aggregate_by_month
from app.utils.gigscore import calculate_gigscore
from app.utils.conflict_resolver import resolve_and_save_income
from app.utils.cert_generator import generate_certificate

router = APIRouter(tags=["upload"])
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/upload/statement")
async def upload_statement(file: UploadFile = File(...), user=Depends(get_current_user)):
    db = get_supabase()

    # ── Step 1: Validate ──────────────────────────────────────
    if user["role"] != "gig_worker":
        raise HTTPException(403, "Only gig workers can upload bank statements.")

    if file.content_type not in ["application/pdf", "application/x-pdf"]:
        raise HTTPException(400, "File must be a PDF.")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(400, "File too large. Maximum size is 10MB.")

    # ── Step 2: Save to temp + create upload record ───────────
    temp_path = f"{TEMP_DIR}/{uuid.uuid4()}.pdf"
    with open(temp_path, "wb") as f:
        f.write(content)

    upload_result = db.table("pdf_uploads").insert({
        "worker_id": user["id"],
        "status": "processing"
    }).execute()
    upload_id = upload_result.data[0]["id"]

    # ── Step 3: Fraud check ───────────────────────────────────
    fraud_result = run_fraud_checks(temp_path)

    if not fraud_result["passed"]:
        os.remove(temp_path)
        db.table("pdf_uploads").update({
            "status": "failed",
            "fraud_check": "failed",
            "fraud_reason": fraud_result["reason"],
            "processed_at": "now()"
        }).eq("id", upload_id).execute()

        raise HTTPException(422, {
            "status": "failed",
            "fraud_check": "failed",
            "reason": fraud_result["reason"],
            "upload_id": upload_id
        })

    # ── Steps 4–5: Extract + aggregate ───────────────────────
    transactions = extract_gig_income(temp_path, "app/config/vpa_config.json")
    by_platform, monthly_totals = aggregate_by_month(transactions)

    if not transactions:
        os.remove(temp_path)
        db.table("pdf_uploads").update({
            "status": "failed",
            "fraud_check": "passed",
            "fraud_reason": "No gig income transactions found in this statement.",
            "processed_at": "now()"
        }).eq("id", upload_id).execute()

        raise HTTPException(422, {
            "status": "failed",
            "reason": "No gig platform payments found. Make sure this is a bank statement with Swiggy, Zomato, Uber, or similar credits.",
            "upload_id": upload_id
        })

    # ── Steps 6–7: Resolve conflicts + save income entries ───
    await resolve_and_save_income(user["id"], by_platform, upload_id, db)

    # ── Step 8: Delete temp file ──────────────────────────────
    os.remove(temp_path)

    # ── Step 9: Calculate GigScore ────────────────────────────
    gigscore_result = calculate_gigscore(monthly_totals)

    # ── Step 10: Generate certificate if threshold met ────────
    cert_id = None
    months_count = len([m for m, amt in monthly_totals.items() if amt > 0])

    if months_count >= 3:
        cert_id = await generate_certificate(user["id"], gigscore_result, db)

    # ── Step 11: Update upload record ────────────────────────
    platforms_found = list(set(txn["platform"] for txn in transactions))
    db.table("pdf_uploads").update({
        "status": "flagged" if fraud_result.get("flagged") else "passed",
        "fraud_check": "flagged" if fraud_result.get("flagged") else "passed",
        "months_found": months_count,
        "platforms_found": platforms_found,
        "processed_at": "now()"
    }).eq("id", upload_id).execute()

    return {
        "status": "success",
        "upload_id": upload_id,
        "months_found": months_count,
        "platforms_found": platforms_found,
        "monthly_avg": round(sum(monthly_totals.values()) / max(len(monthly_totals), 1)),
        "gigscore": gigscore_result["score"],
        "gigscore_label": gigscore_result["label"],
        "fraud_checklist": fraud_result,
        "certificate_id": cert_id
    }


@router.get("/upload/status/{upload_id}")
async def get_upload_status(upload_id: str, user=Depends(get_current_user)):
    db = get_supabase()
    result = db.table("pdf_uploads").select("*") \
        .eq("id", upload_id).eq("worker_id", user["id"]).execute()

    if not result.data:
        raise HTTPException(404, "Upload not found.")

    upload = result.data[0]

    # If passed, also return the latest certificate
    cert_id = None
    if upload["status"] == "passed":
        cert = db.table("certificates").select("cert_id") \
            .eq("worker_id", user["id"]).eq("status", "active") \
            .order("generated_at", desc=True).limit(1).execute()
        if cert.data:
            cert_id = cert.data[0]["cert_id"]

    return {
        "upload_id": upload_id,
        "status": upload["status"],
        "fraud_check": upload["fraud_check"],
        "months_found": upload["months_found"],
        "platforms_found": upload["platforms_found"],
        "certificate_id": cert_id
    }
```

---

## 7. Fraud Stack

### Code: `app/utils/fraud.py`

```python
import pikepdf
from pathlib import Path


SUSPICIOUS_CREATORS = [
    'adobe acrobat', 'foxit', 'nitro', 'pdf editor',
    'smallpdf', 'ilovepdf', 'sejda', 'pdfescape',
    'pdf-xchange', 'master pdf', 'pdfill'
]


def run_fraud_checks(pdf_path: str) -> dict:
    """
    Runs three fraud checks on a PDF using pikepdf.
    Returns a dict with per-check results and a top-level passed bool.

    Hard fail: returns passed=False with reason → delete file, reject upload
    Soft flag: returns passed=True with flagged=True → accept but create fraud_flag record
    """
    result = {
        "passed": False,
        "flagged": False,
        "metadata_check": "FAIL",
        "font_check": "FAIL",
        "edit_history_check": "FAIL",
        "reason": None
    }

    try:
        pdf = pikepdf.open(pdf_path)

        # ── Check 1: Creator metadata ─────────────────────────
        # Genuine bank-generated PDFs are created by banking software, not PDF editors
        metadata = pdf.docinfo
        creator = str(metadata.get('/Creator', '')).lower()
        producer = str(metadata.get('/Producer', '')).lower()
        combined = creator + ' ' + producer

        if any(tool in combined for tool in SUSPICIOUS_CREATORS):
            result["reason"] = "Document appears to have been edited with a PDF editor."
            return result

        result["metadata_check"] = "PASS"

        # ── Check 2: Font count ───────────────────────────────
        # Genuine bank statements use 2–4 fonts consistently.
        # Injected text typically adds new fonts to individual pages.
        fonts_found = set()
        for page in pdf.pages:
            if '/Resources' in page:
                resources = page['/Resources']
                if '/Font' in resources:
                    for font_name in resources['/Font']:
                        fonts_found.add(str(font_name))

        if len(fonts_found) > 8:
            result["reason"] = f"Unusual font count ({len(fonts_found)}) — possible text injection."
            return result

        result["font_check"] = "PASS"

        # ── Check 3: Edit history via XMP metadata ────────────
        # If a PDF was modified after creation, the XMP dates will differ.
        try:
            if '/XMP' in pdf.Root:
                xmp = pdf.Root['/XMP'].read_bytes().decode('utf-8', errors='ignore')
                if 'xmp:ModifyDate' in xmp and 'xmp:CreateDate' in xmp:
                    create_date = xmp.split('xmp:CreateDate>')[1].split('<')[0][:10]
                    modify_date = xmp.split('xmp:ModifyDate>')[1].split('<')[0][:10]
                    if modify_date > create_date:
                        result["reason"] = "Document was modified after its original creation date."
                        return result
        except Exception:
            pass  # If XMP is unreadable, skip this check — don't penalise the user

        result["edit_history_check"] = "PASS"
        result["passed"] = True
        return result

    except pikepdf.PdfError as e:
        result["reason"] = f"Could not read PDF: {str(e)}"
        return result
    except Exception as e:
        result["reason"] = f"Unexpected error during fraud check: {str(e)}"
        return result
```

### Fraud check thresholds summary

| Check | Tool | Threshold | Action |
|---|---|---|---|
| Creator metadata | pikepdf | Known editor in Creator/Producer | Hard reject |
| Font count | pikepdf | > 8 distinct fonts | Hard reject |
| Edit history | pikepdf XMP | ModifyDate > CreateDate | Hard reject |
| Income divergence | DB compare | > 15% same month two uploads | Flag + accept |
| Income volume | Rule | > ₹1,50,000/month single platform | Flag + accept |
| Zero transactions | pdfplumber | 0 gig credits found | Soft reject with guidance |

---

## 8. VPA Extraction & Monthly Aggregation

### Code: `app/utils/vpa_parser.py`

```python
import pdfplumber
import json
import re
from collections import defaultdict
from pathlib import Path


def load_vpa_lookup(config_path: str) -> dict:
    """Returns a dict: vpa_string_lowercase → platform_name"""
    with open(config_path) as f:
        config = json.load(f)
    lookup = {}
    for platform in config["platforms"]:
        for vpa in platform["vpas"]:
            lookup[vpa.lower()] = platform["name"]
    return lookup


def extract_gig_income(pdf_path: str, config_path: str) -> list:
    """
    Scans all pages and tables in a bank statement PDF.
    Returns a list of gig transactions:
    [{ date, platform, amount_inr, raw_description }]
    """
    vpa_lookup = load_vpa_lookup(config_path)
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row:
                        continue
                    row_text = ' '.join([str(cell) for cell in row if cell])
                    row_lower = row_text.lower()

                    # Match any known VPA (substring match, case-insensitive)
                    matched_platform = None
                    for vpa, platform in vpa_lookup.items():
                        if vpa in row_lower:
                            matched_platform = platform
                            break

                    if not matched_platform:
                        continue

                    # Extract amount — matches formats: 1,234.56 or 1234.56
                    amounts = re.findall(r'[\d,]+\.\d{2}', row_text)
                    if not amounts:
                        continue

                    # Last amount in row is typically the credit column
                    amount_str = amounts[-1].replace(',', '')
                    try:
                        amount = float(amount_str)
                        if amount <= 0:
                            continue
                    except ValueError:
                        continue

                    # Extract date — handles DD/MM/YYYY and DD-MM-YYYY
                    date_match = re.search(r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})', row_text)
                    if not date_match:
                        continue

                    day, month, year = date_match.groups()
                    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                    transactions.append({
                        "date": date_str,
                        "platform": matched_platform,
                        "amount_inr": int(amount),
                        "raw_description": row_text[:200]
                    })

    return transactions


def aggregate_by_month(transactions: list) -> tuple[dict, dict]:
    """
    Groups transactions by month and platform.

    Returns:
      by_platform: { "2025-01": { "Swiggy": 12000, "Zomato": 9000 } }
      monthly_totals: { "2025-01": 21000 }
    """
    by_platform = defaultdict(lambda: defaultdict(int))

    for txn in transactions:
        month = txn["date"][:7]  # "YYYY-MM"
        by_platform[month][txn["platform"]] += txn["amount_inr"]

    monthly_totals = {
        month: sum(platforms.values())
        for month, platforms in by_platform.items()
    }

    return dict(by_platform), monthly_totals
```

---

## 9. GigScore Algorithm

GigScore is a 0–100 score representing income reliability. Judges will ask how it works — know this by heart.

**Four components:**
- **Consistency (50%)** — inverse of income variance. Zero variance = 100, high variance = 0
- **Completeness (35%)** — how many of the 6-month window have non-zero income
- **Gap penalty** — 10 points deducted per zero month
- **Recency bonus (+5)** — if recent 3 months ≥ 90% of older 3 months average

### Code: `app/utils/gigscore.py`

```python
import statistics
from typing import Optional


LABELS = [
    (85, "Excellent"),
    (70, "Good"),
    (55, "Moderate"),
    (40, "Low"),
    (0,  "Insufficient")
]


def calculate_gigscore(monthly_totals: dict) -> dict:
    """
    monthly_totals: { "2025-01": 21000, "2025-02": 18000, ... }
    Returns: { score, label, inputs }
    """
    if not monthly_totals:
        return {"score": 0, "label": "Insufficient", "inputs": {}}

    # Build the 6-month window (most recent 6 months)
    sorted_months = sorted(monthly_totals.keys(), reverse=True)
    window = sorted_months[:6]
    all_amounts = [monthly_totals.get(m, 0) for m in window]

    months_with_income = len([a for a in all_amounts if a > 0])
    months_with_zero = len(all_amounts) - months_with_income

    if months_with_income == 0:
        return {"score": 0, "label": "Insufficient", "inputs": {}}

    mean_income = statistics.mean(all_amounts)
    std_dev = statistics.stdev(all_amounts) if len(all_amounts) > 1 else 0
    cv = std_dev / mean_income if mean_income > 0 else 1.0

    # Component A: Consistency (0–100, inverse of CV)
    consistency_score = max(0, 100 - (cv * 100))

    # Component B: Completeness (0–100)
    completeness_score = (months_with_income / 6) * 100

    # Component C: Gap penalty
    gap_penalty = months_with_zero * 10

    # Component D: Recency bonus
    recency_bonus = 0
    if len(all_amounts) >= 6:
        recent_mean = statistics.mean(all_amounts[:3])
        older_mean = statistics.mean(all_amounts[3:])
        if older_mean > 0 and recent_mean >= older_mean * 0.9:
            recency_bonus = 5

    # Combine with weights
    raw_score = (
        (consistency_score * 0.50) +
        (completeness_score * 0.35) +
        recency_bonus
    ) - gap_penalty

    final_score = max(0, min(100, round(raw_score)))

    # Assign label
    label = "Insufficient"
    for threshold, lbl in LABELS:
        if final_score >= threshold:
            label = lbl
            break

    return {
        "score": final_score,
        "label": label,
        "inputs": {
            "months_in_window": len(window),
            "months_with_income": months_with_income,
            "mean_income_inr": round(mean_income),
            "coefficient_of_variation": round(cv, 3),
            "consistency_score": round(consistency_score),
            "completeness_score": round(completeness_score),
            "gap_penalty": gap_penalty,
            "recency_bonus": recency_bonus
        }
    }
```

---

## 10. Conflict Resolution

When a new upload covers months that already have income records, apply these rules:

### Code: `app/utils/conflict_resolver.py`

```python
from app.config.database import get_supabase


async def resolve_and_save_income(
    worker_id: str,
    by_platform: dict,
    upload_id: str,
    db
) -> list:
    """
    Merges new income data with existing records.
    
    Rules:
    - PDF upload: newer data always wins. Flag if > 15% divergence.
    - Razorpay payouts: always additive, never replace.
    
    Returns list of months that were updated (for worker notification).
    """
    updated_months = []

    for month, platforms in by_platform.items():
        for platform, amount in platforms.items():

            # Check if an entry already exists for this month + platform
            existing = db.table("income_entries").select("*") \
                .eq("worker_id", worker_id) \
                .eq("month", month) \
                .eq("platform", platform) \
                .execute()

            if existing.data:
                old_entry = existing.data[0]
                old_amount = old_entry["amount_inr"]

                # Calculate divergence
                divergence = abs(amount - old_amount) / max(old_amount, 1)

                if divergence > 0.15:
                    # Flag for manual review — but still accept the newer figure
                    db.table("fraud_flags").insert({
                        "worker_id": worker_id,
                        "upload_id": upload_id,
                        "flag_type": "income_divergence",
                        "flag_reason": (
                            f"Month {month} ({platform}): income changed by "
                            f"{round(divergence * 100)}% between two uploads "
                            f"(₹{old_amount:,} → ₹{amount:,})"
                        )
                    }).execute()

                # Always update to newer figure
                db.table("income_entries").update({
                    "amount_inr": amount,
                    "source_ref": upload_id
                }).eq("id", old_entry["id"]).execute()

                updated_months.append(month)

            else:
                # No existing entry — insert fresh
                db.table("income_entries").insert({
                    "worker_id": worker_id,
                    "month": month,
                    "platform": platform,
                    "amount_inr": amount,
                    "source_type": "pdf_upload",
                    "source_ref": upload_id,
                    "household_id": None
                }).execute()

    return updated_months
```

---

## 11. Certificate Generation

### Code: `app/utils/cert_generator.py`

```python
import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm
from app.config.database import get_supabase

CERT_DIR = "certificates"
os.makedirs(CERT_DIR, exist_ok=True)

# Brand colors
GREEN = colors.HexColor("#10B981")
BLACK = colors.HexColor("#000000")
DARK_GREY = colors.HexColor("#374151")
LIGHT_GREY = colors.HexColor("#F3F4F6")


def _get_next_cert_id() -> str:
    db = get_supabase()
    result = db.rpc("nextval", {"sequence_name": "cert_sequence"}).execute()
    seq = result.data if result.data else 1
    year = datetime.now().year
    return f"CW-{year}-{str(seq).zfill(5)}"


def _should_regenerate(worker_id: str, new_score: int, new_avg: int, db) -> tuple[bool, int]:
    """Returns (should_regenerate, next_version)"""
    existing = db.table("certificates").select("*") \
        .eq("worker_id", worker_id) \
        .eq("status", "active") \
        .order("version", desc=True) \
        .limit(1).execute()

    if not existing.data:
        return True, 1

    current = existing.data[0]
    score_change = abs(new_score - current["gigscore"]) / max(current["gigscore"], 1)
    income_change = abs(new_avg - current["monthly_avg_inr"]) / max(current["monthly_avg_inr"], 1)

    if score_change > 0.05 or income_change > 0.05:
        return True, current["version"] + 1

    return False, current["version"]


async def generate_certificate(worker_id: str, gigscore_result: dict, db) -> str | None:
    """
    Generates a PDF certificate for a worker if thresholds are met.
    Returns cert_id if generated, None otherwise.
    """
    # Fetch all income entries for this worker (6-month window)
    income_rows = db.table("income_entries").select("*") \
        .eq("worker_id", worker_id) \
        .order("month", desc=True) \
        .limit(100).execute()

    if not income_rows.data:
        return None

    # Build monthly breakdown
    monthly_map = {}
    for row in income_rows.data:
        m = row["month"]
        if m not in monthly_map:
            monthly_map[m] = {"amount": 0, "platforms": set(), "household": row.get("household_id")}
        monthly_map[m]["amount"] += row["amount_inr"]
        if row.get("platform"):
            monthly_map[m]["platforms"].add(row["platform"])

    # Take most recent 6 months with income
    sorted_months = sorted(
        [(m, d) for m, d in monthly_map.items() if d["amount"] > 0],
        reverse=True
    )[:6]

    if len(sorted_months) < 3:
        return None

    monthly_avg = round(sum(d["amount"] for _, d in sorted_months) / len(sorted_months))
    should_gen, version = _should_regenerate(worker_id, gigscore_result["score"], monthly_avg, db)

    if not should_gen:
        return None

    # Fetch worker details
    worker = db.table("users").select("*").eq("id", worker_id).execute().data[0]

    cert_id = _get_next_cert_id()
    period_start = sorted_months[-1][0]
    period_end = sorted_months[0][0]
    pdf_filename = f"{CERT_DIR}/{cert_id}.pdf"

    # ── Build PDF ─────────────────────────────────────────────
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    story = []

    # Header
    story.append(Paragraph(
        "<font color='#10B981'><b>Credwork</b></font>",
        ParagraphStyle("brand", fontSize=28, spaceAfter=4)
    ))
    story.append(Paragraph(
        "Income Verification Certificate",
        ParagraphStyle("title", fontSize=16, textColor=DARK_GREY, spaceAfter=2)
    ))
    story.append(Paragraph(
        f"Certificate ID: <b>{cert_id}</b>  |  Version {version}",
        ParagraphStyle("certid", fontSize=10, textColor=DARK_GREY, spaceAfter=12)
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=GREEN, spaceAfter=16))

    # Worker details
    story.append(Paragraph(f"<b>{worker['full_name']}</b>", styles["Heading2"]))
    story.append(Paragraph(f"{worker['city']} &nbsp;|&nbsp; Member since {worker['created_at'][:7]}", styles["Normal"]))
    story.append(Spacer(1, 16))

    # GigScore box
    score_label_color = "#10B981" if gigscore_result["score"] >= 70 else "#F59E0B" if gigscore_result["score"] >= 55 else "#EF4444"
    story.append(Table(
        [[
            f"GigScore: {gigscore_result['score']}/100",
            gigscore_result["label"],
            f"₹{monthly_avg:,}/month avg"
        ]],
        colWidths=[5.5*cm, 4*cm, 5.5*cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("FONTSIZE", (0, 0), (-1, -1), 13),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GREY]),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    ))
    story.append(Spacer(1, 20))

    # Monthly breakdown table
    story.append(Paragraph("<b>Verified Income Breakdown</b>", styles["Heading3"]))
    story.append(Spacer(1, 8))

    table_data = [["Month", "Platform(s)", "Amount (₹)"]]
    for month, data in sorted_months:
        dt = datetime.strptime(month, "%Y-%m")
        month_label = dt.strftime("%B %Y")
        platforms = ", ".join(data["platforms"]) if data["platforms"] else "ServiConnect"
        table_data.append([month_label, platforms, f"₹{data['amount']:,}"])

    table_data.append(["", "6-Month Average", f"₹{monthly_avg:,}"])

    story.append(Table(
        table_data,
        colWidths=[5*cm, 7*cm, 4*cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLACK),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, LIGHT_GREY]),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, -1), (-1, -1), LIGHT_GREY),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("ALIGN", (2, 0), (2, -1), "RIGHT"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    ))
    story.append(Spacer(1, 20))

    # Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E5E7EB"), spaceAfter=10))
    story.append(Paragraph(
        f"Issued: {datetime.now().strftime('%d %B %Y')} &nbsp;|&nbsp; "
        f"Period: {period_start} to {period_end} &nbsp;|&nbsp; "
        f"Verify: credwork.in/verify/{cert_id}",
        ParagraphStyle("footer", fontSize=8, textColor=DARK_GREY)
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This certificate was generated by Credwork based on verified bank statement UPI transaction data. "
        "This is not a credit guarantee. Lenders should use this as one input in their credit assessment.",
        ParagraphStyle("disclaimer", fontSize=7, textColor=colors.HexColor("#9CA3AF"))
    ))

    doc.build(story)

    # ── Supersede old certificate, save new one ───────────────
    db.table("certificates").update({"status": "superseded"}) \
        .eq("worker_id", worker_id).eq("status", "active").execute()

    months_included = [
        {
            "month": m,
            "amount": d["amount"],
            "platforms": list(d["platforms"]) or None
        }
        for m, d in sorted_months
    ]

    db.table("certificates").insert({
        "cert_id": cert_id,
        "worker_id": worker_id,
        "version": version,
        "status": "active",
        "period_start": period_start,
        "period_end": period_end,
        "monthly_avg_inr": monthly_avg,
        "gigscore": gigscore_result["score"],
        "gigscore_label": gigscore_result["label"],
        "months_included": months_included,
        "pdf_url": f"/certificates/{cert_id}/pdf"
    }).execute()

    return cert_id
```

---

## 12. ServiConnect — Household Payment Flow

### Add worker to household

```
POST /household/add-worker
Auth: Bearer access_token (household role)
Body: {
  worker_phone: "9876543210",
  worker_role: "Cook",
  monthly_salary: 3500,
  payment_day: 1
}

Logic:
1. Look up user by phone where role = 'domestic_worker'
2. Found → create household_workers record
3. Not found → create placeholder + log invite (stub SMS for demo)

Response:
{ status: "linked" | "invited", worker_id, household_worker_id }
```

### Make a payment

```
POST /household/payment
Auth: Bearer access_token (household role)
Body: {
  worker_id: "uuid",
  amount_inr: 3500,
  payment_type: "salary",
  payment_month: "2025-03"
}

Logic:
1. Validate household_workers link is active
2. Validate payment_month (backdating rules below)
3. Create payment record (status: pending)
4. Fire simulate_razorpay_webhook() in background
5. Return payment_id

Response: { payment_id: "uuid", status: "pending" }
```

### Backdating rules

```python
def validate_payment_month(payment_month: str, worker_id: str, db) -> bool:
    from datetime import datetime

    now = datetime.now()
    current_month = now.strftime('%Y-%m')

    if payment_month == current_month:
        return True  # Current month always allowed

    payment_date = datetime.strptime(payment_month + '-01', '%Y-%m-%d')
    days_ago = (now - payment_date).days

    if days_ago <= 30:
        # Check: max 1 backdated entry per 6-month history
        count_result = db.table("payments").select("id", count="exact") \
            .eq("worker_id", worker_id) \
            .lt("payment_month", current_month) \
            .gte("created_at", (now.replace(month=now.month - 6)).isoformat()) \
            .execute()
        return (count_result.count or 0) < 1

    return False  # More than 30 days — not allowed
```

---

## 13. Razorpay Simulation

**Do not integrate real Razorpay by the 16th. Use this simulation exactly.**

### Code: `app/utils/razorpay_sim.py`

```python
import asyncio
import uuid
from app.config.database import get_supabase
from app.utils.gigscore import calculate_gigscore
from app.utils.cert_generator import generate_certificate


async def simulate_razorpay_webhook(payment_id: str):
    """
    Simulates a Razorpay payout webhook.
    Called as a background task after payment creation.
    The 3-second delay makes the demo feel like a real payment is processing.
    """
    await asyncio.sleep(3)

    db = get_supabase()
    payment_result = db.table("payments").select("*").eq("id", payment_id).execute()

    if not payment_result.data:
        return

    payment = payment_result.data[0]

    if payment["status"] != "pending":
        return  # Already processed — idempotency guard

    fake_payout_id = f"pout_{uuid.uuid4().hex[:16]}"

    # Mark payment as processed
    db.table("payments").update({
        "status": "processed",
        "razorpay_ref": fake_payout_id
    }).eq("id", payment_id).execute()

    # Create or update income entry for worker
    existing = db.table("income_entries").select("*") \
        .eq("worker_id", payment["worker_id"]) \
        .eq("month", payment["payment_month"]) \
        .eq("household_id", payment["household_id"]) \
        .execute()

    if existing.data:
        # Payments are additive — stack them (salary + bonus in same month)
        new_amount = existing.data[0]["amount_inr"] + payment["amount_inr"]
        db.table("income_entries").update({
            "amount_inr": new_amount
        }).eq("id", existing.data[0]["id"]).execute()
    else:
        db.table("income_entries").insert({
            "worker_id": payment["worker_id"],
            "month": payment["payment_month"],
            "household_id": payment["household_id"],
            "amount_inr": payment["amount_inr"],
            "source_type": "razorpay_payout",
            "source_ref": fake_payout_id,
            "platform": None
        }).execute()

    # Recalculate GigScore and regenerate certificate if needed
    all_income = db.table("income_entries").select("month, amount_inr") \
        .eq("worker_id", payment["worker_id"]).execute()

    monthly_totals = {}
    for row in all_income.data:
        m = row["month"]
        monthly_totals[m] = monthly_totals.get(m, 0) + row["amount_inr"]

    gigscore_result = calculate_gigscore(monthly_totals)
    await generate_certificate(payment["worker_id"], gigscore_result, db)
```

---

## 14. All API Endpoints

```
AUTH
  POST   /auth/send-otp
  POST   /auth/verify-otp
  POST   /auth/setup-profile
  GET    /auth/me
  PUT    /auth/me
  DELETE /auth/me

GIG WORKER
  POST   /upload/statement
  GET    /upload/status/{upload_id}
  GET    /worker/dashboard
  GET    /worker/income

CERTIFICATES
  GET    /certificates
  GET    /certificates/{cert_id}
  GET    /certificates/{cert_id}/pdf
  GET    /verify/{cert_id}              ← PUBLIC, no auth required
  POST   /certificates/{cert_id}/share

HOUSEHOLD
  GET    /household/dashboard
  POST   /household/add-worker
  GET    /household/workers
  DELETE /household/workers/{id}
  POST   /household/payment
  GET    /household/payment-status/{payment_id}
  GET    /household/payments
  GET    /household/payments/{worker_id}

DOMESTIC WORKER
  GET    /worker/dashboard              ← Same endpoint, role determines response
  GET    /worker/payments
  GET    /worker/household

SETTINGS
  PUT    /settings/language
  PUT    /settings/notifications
  GET    /settings/data-export

ADMIN (no auth for demo — add API key header post-launch)
  GET    /admin/stats
  GET    /admin/uploads
  GET    /admin/fraud-flags
  GET    /admin/certificates
  GET    /admin/payments
  POST   /admin/fraud-flags/{id}/review
```

---

## 15. VPA Config

Save as `app/config/vpa_config.json`.

```json
{
  "version": "1.0",
  "last_updated": "2025-03-12",
  "note": "VPA matching is case-insensitive substring match. Add new VPAs as you discover them from real bank statements.",
  "platforms": [
    {
      "name": "Swiggy",
      "category": "delivery",
      "vpas": ["swiggy@icici", "swiggy@yesbank", "swiggy@ybl", "delivery@swiggy", "swiggyit@icici", "eazypay@icici"]
    },
    {
      "name": "Zomato",
      "category": "delivery",
      "vpas": ["zomato@icici", "zomato@hdfcbank", "zomato@kotak", "delivery@zomato", "zomatoonline@icici"]
    },
    {
      "name": "Uber",
      "category": "ride_hailing",
      "vpas": ["uber@axis", "uber@hdfcbank", "uber@icici", "uberdriver@icici"]
    },
    {
      "name": "Ola",
      "category": "ride_hailing",
      "vpas": ["ola@icici", "olacabs@icici", "ani@icici"]
    },
    {
      "name": "Rapido",
      "category": "ride_hailing",
      "vpas": ["rapido@ybl", "rapido@icici", "roppen@icici", "rapidobikeapp@icici"]
    },
    {
      "name": "Blinkit",
      "category": "quick_commerce",
      "vpas": ["blinkit@icici", "grofers@icici", "blinkit@yesbank"]
    },
    {
      "name": "Zepto",
      "category": "quick_commerce",
      "vpas": ["zepto@icici", "kiranaclub@icici"]
    },
    {
      "name": "Urban Company",
      "category": "home_services",
      "vpas": ["urbanclap@icici", "urbancompany@icici", "uc@razorpay"]
    },
    {
      "name": "Dunzo",
      "category": "delivery",
      "vpas": ["dunzo@icici", "dunzodaily@icici"]
    }
  ]
}
```

---

## 16. Vercel Deployment

### `vercel.json` in project root

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

### `main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import auth, upload, worker, certificates, household, settings, admin

app = FastAPI(
    title="Credwork API",
    description="Income verification for India's gig and domestic workers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten post-launch
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated certificates as static files
os.makedirs("certificates", exist_ok=True)
app.mount("/certificates", StaticFiles(directory="certificates"), name="certificates")

# Register all routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(worker.router)
app.include_router(certificates.router)
app.include_router(household.router)
app.include_router(settings.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {
        "name": "Credwork API",
        "version": "1.0.0",
        "status": "live",
        "docs": "/docs"
    }
```

### Deploy

```bash
npm i -g vercel
vercel login
vercel --prod
```

Add all `.env` variables in Vercel dashboard → Settings → Environment Variables.

---

## 17. Demo Seed Data

Run this before the demo to pre-populate two demo accounts.

```python
# seed.py — run once: python seed.py

from app.config.database import get_supabase
from app.utils.auth_helpers import create_access_token

db = get_supabase()

# ── Demo Account 1: Gig Worker ────────────────────────────────
gig_user = db.table("users").insert({
    "phone": "9999900001",
    "role": "gig_worker",
    "full_name": "Raju Kumar",
    "city": "Mumbai",
    "language": "hi",
    "is_verified": True
}).execute().data[0]

income_data = [
    ("2024-10", "Swiggy", 11200),
    ("2024-10", "Blinkit", 6000),
    ("2024-11", "Swiggy", 12800),
    ("2024-11", "Zomato", 7000),
    ("2024-12", "Swiggy", 10500),
    ("2024-12", "Rapido", 5000),
    ("2025-01", "Swiggy", 13000),
    ("2025-01", "Zomato", 8000),
    ("2025-02", "Swiggy", 12400),
    ("2025-02", "Blinkit", 6500),
    ("2025-03", "Swiggy", 11600),
    ("2025-03", "Zomato", 7500),
]

for month, platform, amount in income_data:
    db.table("income_entries").insert({
        "worker_id": gig_user["id"],
        "month": month,
        "platform": platform,
        "amount_inr": amount,
        "source_type": "pdf_upload",
        "source_ref": "demo_seed"
    }).execute()

print(f"Gig worker token: {create_access_token(gig_user['id'], 'gig_worker', '9999900001')}")

# ── Demo Account 2: Domestic Worker + Household ───────────────
domestic_user = db.table("users").insert({
    "phone": "9999900002",
    "role": "domestic_worker",
    "full_name": "Priya Devi",
    "city": "New Delhi",
    "language": "hi",
    "is_verified": True
}).execute().data[0]

household_user = db.table("users").insert({
    "phone": "9999900003",
    "role": "household",
    "full_name": "Sharma Household",
    "city": "New Delhi",
    "language": "en",
    "is_verified": True
}).execute().data[0]

db.table("household_workers").insert({
    "household_id": household_user["id"],
    "worker_id": domestic_user["id"],
    "worker_role": "Cook",
    "monthly_salary": 3500,
    "payment_day": 1,
    "is_active": True
}).execute()

domestic_payments = [
    ("2024-10", 3000),
    ("2024-11", 3500),
    ("2024-12", 4000),
    ("2025-01", 3500),
    ("2025-02", 3500),
]

for month, amount in domestic_payments:
    db.table("income_entries").insert({
        "worker_id": domestic_user["id"],
        "month": month,
        "household_id": household_user["id"],
        "amount_inr": amount,
        "source_type": "razorpay_payout",
        "source_ref": "demo_seed",
        "platform": None
    }).execute()

print(f"Domestic worker token: {create_access_token(domestic_user['id'], 'domestic_worker', '9999900002')}")
print(f"Household token: {create_access_token(household_user['id'], 'household', '9999900003')}")
print("Seed complete.")
```

---

## 18. What to Stub vs What Must Be Real

### Must be real on demo day — judges will test these

| Feature | Why |
|---|---|
| PDF fraud detection | Judges will bring a fake PDF to test |
| VPA extraction | Must work on a real bank statement |
| GigScore calculation | Judges will ask how it's calculated |
| Certificate PDF download | Must be real, downloadable, look professional |
| `GET /verify/{cert_id}` | Judges will open this URL |
| ServiConnect full loop | Household pays → worker record updates → cert changes live |

### Safe to stub — won't affect the demo

| Feature | Stub approach |
|---|---|
| SMS OTP sending | Print to console, hardcode "123456" for demo phones |
| PDF file storage | Local `/certificates` folder instead of S3 |
| Real Razorpay webhooks | Use `simulate_razorpay_webhook()` from Section 13 |
| Push notifications | UI toggles only, no actual sending |
| DPDP data export | Return JSON of user's data, no formatted PDF needed |
| Admin auth | No auth on `/admin/*` for hackathon |

---

*Credwork Backend v1.0 — built for the hackathon, designed to scale.*
*All business logic in this document is final. Any deviations must be discussed with the full team.*
