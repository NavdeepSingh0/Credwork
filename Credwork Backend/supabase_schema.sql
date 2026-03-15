-- ============================================================
-- CREDWORK — COMPLETE SUPABASE SCHEMA
-- Run this ONCE in Supabase SQL Editor (https://supabase.com/dashboard → SQL Editor)
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ──────────────────────────────────────────────────────────────
-- 1. USERS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone       TEXT UNIQUE NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('gig_worker', 'domestic_worker', 'household')),
    full_name   TEXT NOT NULL,
    city        TEXT,
    photo_url   TEXT,
    language    TEXT DEFAULT 'en',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 2. OTP SESSIONS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS otp_sessions (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone       TEXT NOT NULL,
    otp_hash    TEXT NOT NULL,
    expires_at  TIMESTAMPTZ NOT NULL,
    verified    BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 3. PDF UPLOADS (includes Phase 7B ML columns)
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pdf_uploads (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    worker_id             UUID REFERENCES users(id),
    status                TEXT DEFAULT 'processing',
    fraud_check           TEXT,
    fraud_reason          TEXT,
    months_found          INT,
    platforms_found       JSONB,
    processed_at          TIMESTAMPTZ,
    -- Phase 7B: ML anomaly detection columns
    ml_anomaly_detected   BOOLEAN DEFAULT FALSE,
    ml_anomaly_score      FLOAT,
    ml_model_confidence   FLOAT,
    ml_anomaly_note       TEXT,
    created_at            TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 4. INCOME ENTRIES
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS income_entries (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    worker_id    UUID REFERENCES users(id),
    month        TEXT NOT NULL,           -- "YYYY-MM"
    platform     TEXT,                    -- "Swiggy", "Zomato", etc. NULL for domestic
    amount_inr   INT NOT NULL,
    source_type  TEXT NOT NULL,           -- "pdf_upload" or "razorpay_payout"
    source_ref   TEXT,                    -- upload_id or "demo_seed"
    household_id UUID REFERENCES users(id),
    created_at   TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 5. CERTIFICATES
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS certificates (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cert_id         TEXT UNIQUE NOT NULL,  -- "CW-2025-00001"
    worker_id       UUID REFERENCES users(id),
    version         INT DEFAULT 1,
    status          TEXT DEFAULT 'active', -- "active" or "superseded"
    period_start    TEXT,                  -- "YYYY-MM"
    period_end      TEXT,                  -- "YYYY-MM"
    monthly_avg_inr INT,
    gigscore        INT,
    gigscore_label  TEXT,
    months_included JSONB,
    pdf_url         TEXT,
    generated_at    TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 6. FRAUD FLAGS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fraud_flags (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    worker_id   UUID REFERENCES users(id),
    upload_id   UUID REFERENCES pdf_uploads(id),
    flag_type   TEXT NOT NULL,            -- "income_divergence", "ml_anomaly_high", etc.
    flag_reason TEXT,
    status      TEXT DEFAULT 'pending',   -- "pending", "approved", "rejected"
    reviewed_by TEXT,
    review_note TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 7. HOUSEHOLD WORKERS (linking table)
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS household_workers (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    household_id   UUID REFERENCES users(id),
    worker_id      UUID REFERENCES users(id),
    worker_role    TEXT,                   -- "Cook", "Maid", etc.
    monthly_salary INT,
    payment_day    INT,
    is_active      BOOLEAN DEFAULT TRUE,
    created_at     TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 8. PAYMENTS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    household_id   UUID REFERENCES users(id),
    worker_id      UUID REFERENCES users(id),
    amount_inr     INT NOT NULL,
    payment_type   TEXT NOT NULL,          -- "salary", "bonus", "advance"
    payment_month  TEXT NOT NULL,          -- "YYYY-MM"
    payment_date   TEXT,                   -- "YYYY-MM-DD"
    status         TEXT DEFAULT 'pending', -- "pending", "processed", "failed"
    razorpay_id    TEXT,
    created_at     TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 9. CERTIFICATE SEQUENCE (for cert_id generation: CW-YYYY-NNNNN)
-- ──────────────────────────────────────────────────────────────
CREATE SEQUENCE IF NOT EXISTS cert_sequence START 1;

-- Helper function for cert_generator.py to call via RPC
CREATE OR REPLACE FUNCTION nextval(sequence_name TEXT)
RETURNS BIGINT AS $$
BEGIN
    RETURN nextval(sequence_name::regclass);
END;
$$ LANGUAGE plpgsql;

-- ──────────────────────────────────────────────────────────────
-- 10. STORAGE BUCKET for certificates (run separately if needed)
-- ──────────────────────────────────────────────────────────────
-- NOTE: Create this manually in Supabase Dashboard:
-- Storage → New Bucket → name: "certificates" → set as PUBLIC
-- (SQL cannot create storage buckets directly)

-- ============================================================
-- END OF SCHEMA
-- ============================================================
