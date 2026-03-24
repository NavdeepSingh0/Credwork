-- ============================================================
-- CREDWORK — COMPLETE SUPABASE SCHEMA
-- *** THIS FILE REFLECTS THE LIVE DATABASE AS OF 2026-03-24 ***
-- Run this ONCE in Supabase SQL Editor on a fresh project.
-- For existing projects, apply only the delta migrations you need.
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ──────────────────────────────────────────────────────────────
-- 1. USERS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone       VARCHAR UNIQUE NOT NULL,
    role        VARCHAR NOT NULL CHECK (role IN ('gig_worker', 'domestic_worker', 'household', 'admin')),
    full_name   VARCHAR NOT NULL,
    city        VARCHAR,
    language    VARCHAR DEFAULT 'en',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 2. OTP SESSIONS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS otp_sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone       VARCHAR NOT NULL,
    otp_hash    VARCHAR NOT NULL,
    expires_at  TIMESTAMPTZ NOT NULL,
    verified    BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 3. PDF UPLOADS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pdf_uploads (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    worker_id        UUID REFERENCES users(id),
    status           VARCHAR DEFAULT 'processing' CHECK (status IN ('processing', 'passed', 'flagged', 'failed')),
    fraud_check      VARCHAR CHECK (fraud_check IN ('passed', 'flagged', 'failed')),
    fraud_reason     TEXT,
    months_found     INT,
    platforms_found  TEXT[],
    processed_at     TIMESTAMPTZ,
    created_at       TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 4. INCOME ENTRIES
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS income_entries (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    worker_id    UUID REFERENCES users(id),
    month        VARCHAR NOT NULL,           -- "YYYY-MM"
    platform     VARCHAR,                    -- "Swiggy", "Zomato", etc. NULL for domestic
    amount_inr   INT NOT NULL,
    source_type  VARCHAR NOT NULL CHECK (source_type IN ('pdf_upload', 'razorpay_payout', 'manual_entry', 'api_sync')),
    source_ref   VARCHAR,                    -- upload_id or "demo_seed"
    household_id UUID REFERENCES users(id),
    created_at   TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 5. CERTIFICATES
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS certificates (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cert_id         VARCHAR UNIQUE NOT NULL,  -- "CW-2025-00001"
    worker_id       UUID REFERENCES users(id),
    version         INT DEFAULT 1,
    status          VARCHAR DEFAULT 'active' CHECK (status IN ('active', 'superseded')),
    period_start    VARCHAR,                  -- "YYYY-MM"
    period_end      VARCHAR,                  -- "YYYY-MM"
    monthly_avg_inr INT,
    gigscore        INT,
    gigscore_label  VARCHAR,
    months_included JSONB,
    pdf_url         VARCHAR,
    mode            TEXT DEFAULT 'gig',       -- "gig" or "generic"
    generated_at    TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 6. FRAUD FLAGS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fraud_flags (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upload_id    UUID REFERENCES pdf_uploads(id),
    worker_id    UUID REFERENCES users(id),
    flag_type    VARCHAR NOT NULL,
    flag_reason  TEXT NOT NULL,
    admin_status VARCHAR DEFAULT 'pending' CHECK (admin_status IN ('pending', 'approved', 'rejected')),
    reviewed_by  UUID REFERENCES users(id),
    created_at   TIMESTAMPTZ DEFAULT now(),
    resolved_at  TIMESTAMPTZ
);

-- ──────────────────────────────────────────────────────────────
-- 7. HOUSEHOLD WORKERS (linking table)
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS household_workers (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID REFERENCES users(id),
    worker_id      UUID REFERENCES users(id),
    worker_role    VARCHAR,                   -- "Cook", "Maid", etc.
    monthly_salary INT,
    payment_day    INT CHECK (payment_day >= 1 AND payment_day <= 28),
    is_active      BOOLEAN DEFAULT TRUE,
    linked_at      TIMESTAMPTZ DEFAULT now()
);

-- ──────────────────────────────────────────────────────────────
-- 8. PAYMENTS
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id        UUID REFERENCES users(id),
    worker_id           UUID REFERENCES users(id),
    amount_inr          INT NOT NULL,
    payment_type        VARCHAR NOT NULL CHECK (payment_type IN ('salary', 'bonus', 'advance')),
    payment_month       VARCHAR NOT NULL,          -- "YYYY-MM"
    payment_date        TEXT,                      -- "YYYY-MM-DD"
    status              VARCHAR DEFAULT 'pending' CHECK (status IN ('pending', 'processed', 'failed')),
    razorpay_order_id   VARCHAR,
    razorpay_payment_id VARCHAR,
    razorpay_id         TEXT,
    created_at          TIMESTAMPTZ DEFAULT now(),
    processed_at        TIMESTAMPTZ
);

-- ──────────────────────────────────────────────────────────────
-- 9. CERTIFICATE SEQUENCE (for cert_id: CW-YYYY-NNNNN)
-- ──────────────────────────────────────────────────────────────
CREATE SEQUENCE IF NOT EXISTS cert_sequence START 1;

-- RPC wrapper so PostgREST can call it via db.rpc("nextval", ...)
CREATE OR REPLACE FUNCTION public.nextval(sequence_name TEXT)
RETURNS BIGINT AS $$
BEGIN
    RETURN nextval(sequence_name::regclass);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ──────────────────────────────────────────────────────────────
-- 10. STORAGE BUCKET for certificates
-- ──────────────────────────────────────────────────────────────
-- Create manually in Supabase Dashboard OR run the SQL below:
INSERT INTO storage.buckets (id, name, public)
VALUES ('certificates', 'certificates', true)
ON CONFLICT (id) DO NOTHING;

-- Storage policies
CREATE POLICY "Public read access on certificates"
  ON storage.objects FOR SELECT USING (bucket_id = 'certificates');

CREATE POLICY "Service role upload on certificates"
  ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'certificates');

CREATE POLICY "Service role update on certificates"
  ON storage.objects FOR UPDATE USING (bucket_id = 'certificates');

-- ============================================================
-- END OF SCHEMA
-- ============================================================
