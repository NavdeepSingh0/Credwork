# Credwork — Full System Framework & Product Specification

> **Internal Document** | Product & Engineering Reference | v1.0  
> Colour Palette: Primary `#111827` · Secondary `#2563EB` · Accent `#06B6D4` · Background `#F4F6FA`

---

## Table of Contents

1. [The Core Mental Model](#1-the-core-mental-model)
2. [Part 1 — Gig Worker Upload Flow](#2-part-1--gig-worker-upload-flow)
   - 2.1 [First Upload — Establishing the Record](#21-first-upload--establishing-the-record)
   - 2.2 [Subsequent Uploads — The Update Problem](#22-subsequent-uploads--the-update-problem)
3. [Part 2 — Domestic Worker Salary Update Flow (ServiConnect)](#3-part-2--domestic-worker-salary-update-flow-serviconnect)
   - 3.1 [How the Record Builds](#31-how-the-record-builds)
   - 3.2 [What "Updating Salary" Means](#32-what-updating-salary-means)
4. [Part 3 — The Unified Update Logic](#4-part-3--the-unified-update-logic)
5. [Part 4 — Version History and Audit Trail](#5-part-4--version-history-and-audit-trail)
6. [Edge Cases — Must Handle Before Demo Day](#6-edge-cases--must-handle-before-demo-day)
7. [GigScore — Scoring Methodology](#7-gigscore--scoring-methodology)
8. [Colour System & Design Tokens](#8-colour-system--design-tokens)
9. [Summary Mental Model](#9-summary-mental-model)

---

## 1. The Core Mental Model

Think of a worker's income record as a **rolling 6-month window**, not a single snapshot. Every upload or payment either:

- **Extends** that window (new months added),
- **Fills a gap** in it (previously missing months now covered), or
- **Overrides a bad reading** (conflict resolution replacing stale data with newer data).

The certificate — the document Credwork issues to lenders or verification partners — is always a **derivative** of that rolling window. It gets regenerated automatically whenever the window changes in a materially meaningful way.

> **The cleanest mental model:** Uploads and payments are *inputs*. The 6-month rolling window is *state*. The certificate is *output*. Any time inputs change enough to materially affect the state, the output gets regenerated. Everything else is rules for resolving conflicts when inputs contradict each other.

---

## 2. Part 1 — Gig Worker Upload Flow

### 2.1 First Upload — Establishing the Record

When a gig worker uploads for the first time, Credwork is not just parsing a PDF. It is establishing a **baseline identity + income fingerprint** that all future uploads will be compared against. The integrity of this fingerprint is the foundation of the entire trust model.

---

#### Step 1 — PDF Ingestion & Fraud Stack

The worker uploads a bank statement PDF. Before any income data is touched, the **fraud stack runs first**:

| Check | Tool / Method | What It Catches |
|---|---|---|
| Metadata inspection | `pikepdf` | Detect modification timestamps, creator tool mismatches |
| Font consistency check | PDF structure parsing | Detect injected text using inconsistent fonts |
| Edit history analysis | `pikepdf` edit trail | Catch documents that have been opened and re-saved after generation |

**Critical rule:** If a document fails the fraud stack, it is **rejected immediately and never stored** — not even temporarily. Storing a flagged document, even to log it, creates a legal and compliance liability.

---

#### Step 2 — VPA Extraction

After fraud clearance, Credwork scans all credit transactions in the statement and filters for **known gig economy Virtual Payment Addresses (VPAs)** from the `vpa_config.json` configuration file.

Each matching transaction is tagged with:
- **Platform** (e.g., Swiggy, Zomato, Blinkit, Rapido, Urban Company)
- **Amount** (in INR)
- **Transaction date**

Non-gig credits — family transfers, refunds, salary credits from other employers — are **separated out and not counted**, but their existence is noted. This supports downstream fraud detection (e.g., a worker claiming only gig income but receiving large regular NEFT credits warrants a flag).

---

#### Step 3 — Monthly Aggregation

Tagged transactions are grouped by **calendar month** and summed **per platform per month**.

**Example:**
> Raju receives ₹12,000 from Swiggy and ₹9,000 from Zomato in January.  
> January's total gig income = ₹21,000.

**Minimum data thresholds:**

| Months of Data | Certificate Status |
|---|---|
| < 3 months | No certificate issued |
| 3–5 months | Basic certificate issued (limited stability signal) |
| 6 months | Full certificate issued with complete GigScore |

---

#### Step 4 — GigScore Calculation

The **GigScore** is Credwork's proprietary Income Stability Score. It answers a fundamentally different question than average income: *how predictable is this worker's income?*

A worker earning ₹20,000 every month is measurably more reliable than one earning ₹5,000 one month and ₹35,000 the next — even if the 6-month average is identical.

**GigScore factors:**

1. **Variance penalty** — High month-to-month income variance reduces the score. Measured using coefficient of variation (CV = σ/μ). Higher CV = larger penalty.
2. **Consistency reward** — Workers whose income stays within a tight band around their average are rewarded. A ±10% band = high reward; ±50% band = low reward.
3. **History depth factor** — 6 months of history scores higher than 3 months at the same average and variance. The score is scaled by data completeness. This prevents a single high-income month from generating an inflated GigScore.
4. **Gap penalty** — Months with zero income are recorded as zero (not excluded). Zero months compress the average and increase variance.

> **GigScore is not income. GigScore is reliability.**

---

#### Step 5 — Certificate Generation

If minimum thresholds are met (3+ months of data, income within realism bounds), Credwork generates the certificate.

**What gets stored:**

- The underlying **monthly data records** (not just the certificate PDF), because subsequent uploads will need to merge with this data.
- The certificate itself as a versioned PDF.
- The GigScore and the inputs used to compute it.
- The list of VPA matches and their source transactions.

---

### 2.2 Subsequent Uploads — The Update Problem

When a worker uploads a new PDF, Credwork must determine how it relates to the existing record. There are **four distinct scenarios**:

---

#### Scenario A — Newer Period, No Overlap

**Example:** Worker uploaded Jan–June previously. Now uploads July–September.

**Action:** Append new months to the record. Recalculate the rolling 6-month window (now April–September). Regenerate certificate.

This is the clean path — no conflict resolution needed.

---

#### Scenario B — Overlapping Period

**Example:** Worker uploaded Jan–June. Now uploads April–September. Months April, May, June appear in both PDFs.

**Conflict resolution rule:** For any month that appears in both old and new uploads, **trust the newer upload's figures**. The assumption is that newer bank statements are more likely to be final — older statements sometimes contain pending transactions that later settled differently.

**Worker communication:** Flag to the worker that 3 months were updated and show a **before/after comparison** of the figures. Do not silently overwrite.

---

#### Scenario C — Same Period, Different Figures

**Example:** Worker uploads the same month twice, but the income totals differ.

This is either:
- A **legitimate re-upload** (the first PDF was a preliminary or mid-month statement), or
- A **fraud attempt** (figure manipulation between uploads).

**Decision tree:**

| Condition | Action |
|---|---|
| Figures differ by > 15% AND fraud check failed | Reject, flag for review |
| Figures differ by > 15% AND fraud check passed | Flag for manual review — do not auto-accept |
| Figures differ by ≤ 15% AND fraud check passed | Accept newer figure, add note to audit log |

The 15% threshold exists because minor differences between statements are expected (rounding, settlement timing). Large differences require human eyes.

---

#### Scenario D — Gap in History

**Example:** Worker has data for January, February, then nothing for March–April, then May–June.

**Action:** Surface the gap explicitly to the worker:

> *"We noticed a gap in March–April. If you have a bank statement covering those months, upload it to strengthen your certificate."*

Gaps must never be silently ignored. They hurt the GigScore and workers deserve to understand why their score is lower than expected. Transparency about gaps also reduces support tickets and builds trust.

---

## 3. Part 2 — Domestic Worker Salary Update Flow (ServiConnect)

The ServiConnect module within Credwork operates on a **fundamentally different trust model** than the gig worker flow.

In the gig worker flow, Credwork is parsing documents that someone else created (the bank). The primary challenge is verifying authenticity.

In ServiConnect, **Credwork owns the payment truth**. Every payment is made through the platform via Razorpay. There is no document to verify — Credwork is the source of record.

---

### 3.1 How the Record Builds

Every time a household makes a Razorpay payout to a domestic worker, Credwork's backend records:

| Field | Description |
|---|---|
| `amount` | Payment amount in INR |
| `date` | Date of payout |
| `worker_id` | Credwork worker identifier |
| `household_id` | Credwork household identifier |
| `payment_type` | Enum: `salary` / `bonus` / `advance` |

After **3 months of payments**, Credwork has enough data to generate a certificate automatically. No action is required from the worker. No PDF upload. The certificate emerges from actual payment behaviour.

---

### 3.2 What "Updating Salary" Means

There are three distinct update scenarios for domestic workers, each with different rules:

---

#### Scenario 1 — Household Changes the Monthly Pay Rate

The household updates the worker's declared salary (e.g., from ₹3,000/month to ₹3,500/month).

**Rule:** This change is **never retroactive**. Historical payments remain exactly as they were recorded. The new rate applies only to future payments. The certificate reflects actual payment history, not declared rates.

This is important: declared rates are assertions; payment records are facts. Credwork certifies facts.

---

#### Scenario 2 — Missed Month (Cash Payment Not Through Platform)

The household paid the worker in cash for one month and forgot to use ServiConnect. They want to add that month retroactively.

This is a **high fraud-risk operation** because it involves asserting a payment that Credwork did not facilitate or observe.

**Rules:**

| Condition | Action |
|---|---|
| Backdating ≤ 30 days | Allowed, with audit log entry |
| Backdating > 30 days | Not permitted — period is recorded as a gap |
| More than 1 backdated entry in any 6-month window | Blocked — system cap reached |

Both the worker and the household are informed of the cap. Transparency is not optional — if a worker has a gap month because the cap was reached, they need to know and understand why.

---

#### Scenario 3 — Worker Changes Household

A domestic worker leaves one household and joins another.

**Rule:** The worker's payment history from the old household **continues to count toward their certificate**. The income record belongs to the worker, not to the household. The new household's payments are appended to the same worker record.

The certificate reflects total verified income from all households, across the worker's complete Credwork history.

This is critical for worker portability — a worker with 6 months at Household A and 3 months at Household B has a richer, stronger record than either household alone.

---

## 4. Part 3 — The Unified Update Logic

Regardless of worker type (gig or domestic), every income update in Credwork routes through the same downstream pipeline:

```
New data arrives
  └── Source: PDF upload (gig worker)
  └── Source: Razorpay webhook (domestic worker)
            │
            ▼
  ┌─────────────────────────────┐
  │   Fraud / Validity Check    │
  │   (PDF: metadata + font)    │
  │   (Payout: webhook sig)     │
  └────────────┬────────────────┘
               │
               ▼
  ┌────────────────────────────────────────┐
  │       Merge with Existing Record       │
  │  → Apply conflict resolution rules     │
  │  → Scenario A/B/C/D for gig workers    │
  │  → Scenario 1/2/3 for domestic workers │
  └────────────┬───────────────────────────┘
               │
               ▼
  ┌──────────────────────────────────┐
  │  Recalculate 6-Month Rolling     │
  │  Window                          │
  └────────────┬─────────────────────┘
               │
               ▼
  ┌──────────────────────────────────┐
  │   Recalculate GigScore           │
  └────────────┬─────────────────────┘
               │
               ▼
  Has anything changed by more than 5%?
               │
       ┌───────┴────────┐
      YES               NO
       │                 │
       ▼                 ▼
  Regenerate        Update internal
  certificate       record silently.
  Notify worker.    No new cert issued.
       │
       ▼
  Store version in
  certificate history
```

---

### The 5% Threshold — Why It Matters

Without a materiality threshold for regeneration, Credwork would generate a new certificate every time a small transaction is processed — including ₹50 cashback credits or minor corrections. This creates two problems:

1. **Certificate devaluation:** If certificates are issued constantly, lenders stop trusting them as meaningful signals.
2. **Notification fatigue:** Workers would be flooded with "Your certificate has been updated" messages, causing them to ignore all notifications, including important ones.

The 5% threshold means: only changes that materially shift the income picture result in a new certificate and a worker notification.

---

## 5. Part 4 — Version History and Audit Trail

Every certificate Credwork ever issues must be **permanently stored** with a version number and a timestamp. This is non-negotiable.

**Why this matters for lenders:** If a lender has already seen certificate v1 and the worker presents certificate v3, the lender needs to:
- Verify that both certificates are legitimate Credwork-issued documents.
- See exactly what changed between v1 and v3.
- Confirm that v3 supersedes v1 (not that v3 is a fraudulent replacement of v1).

**Why this matters for compliance:** Under audit, Credwork must be able to reconstruct the complete income history for any worker at any point in time.

---

### Data Model

```
WorkerRecord
  ├── income_entries[]
  │     ├── month (YYYY-MM)
  │     ├── platform_or_household_id
  │     ├── amount_inr
  │     └── source
  │           ├── type: "pdf_upload" | "razorpay_payout"
  │           └── reference_id (PDF upload ID or Razorpay payout ID)
  │
  └── certificates[]
        ├── v1
        │     ├── generated_at (ISO 8601 timestamp)
        │     ├── monthly_average_inr
        │     ├── gigscore (0–100)
        │     ├── months_included[]
        │     └── pdf_url (permanent, immutable)
        ├── v2
        │     ├── generated_at
        │     ├── delta_from_v1 (what changed)
        │     ├── monthly_average_inr
        │     ├── gigscore
        │     └── pdf_url
        └── vN ...
```

**Immutability rules:**
- **Never delete** old certificates.
- **Never overwrite** old certificates.
- **Only append** new versions.

Old certificates must remain accessible, individually linkable, and verifiable even after a worker's account has been deactivated.

---

## 6. Edge Cases — Must Handle Before Demo Day

These are not hypothetical — each scenario has occurred in production pilots or is structurally guaranteed to occur at scale.

---

### Case 1 — Worker Uploads 12 Months of Statements at Once

**Rule:** Use only the most recent 6 months for the certificate computation. Store all 12.

**Why store all 12?** Older data strengthens fraud detection. If a worker's income pattern over months 1–6 is completely inconsistent with months 7–12, that inconsistency is a signal worth investigating. Historical data doesn't go into the certificate but does go into the fraud risk model.

---

### Case 2 — Zero-Income Month

A month with zero gig income must be **recorded as zero, not ignored**.

Ignoring a zero month inflates the monthly average artificially. This is a real scenario — workers get sick, take seasonal breaks, or face slow months on the platform. Omitting these months would make Credwork certificates dishonest and would expose lenders to risk based on inflated income representations.

A zero month should also drive a GigScore penalty, because it represents income volatility.

---

### Case 3 — Two Workers Share a Bank Account

Credwork's VPA extraction will pull all gig credits from a shared statement. If two people use the same bank account, the system will double-attribute income to a single worker.

**This cannot be fully resolved without identity verification.** However, Credwork should:
- Flag statements where the aggregate gig income volume is statistically implausible for a single person (e.g., implying 20+ hours of delivery work per day).
- Surface a manual review flag: *"Income volume may reflect multiple earners sharing this account."*

---

### Case 4 — Worker Deletes Their Credwork Account

Under the **Digital Personal Data Protection (DPDP) Act**, a worker has the right to request deletion of their personal data.

**Critical nuance:** Certificates already issued to lenders cannot be recalled from lender systems.

Credwork's privacy policy and in-app disclosure must be explicit at the time of certificate issuance:

> *"Once your income certificate is shared with a lender or verification partner, it persists in their systems independent of your Credwork account. Deleting your Credwork account does not recall certificates already shared."*

This must be presented as a pre-sharing consent screen, not buried in terms of service.

---

## 7. GigScore — Scoring Methodology

The GigScore replaces the generic term "Income Stability Score" across all of Credwork's products, interfaces, certificates, and API responses.

### Score Range

| GigScore Range | Label | Interpretation |
|---|---|---|
| 85–100 | Excellent | Highly consistent income over 6 months |
| 70–84 | Good | Solid income with minor variability |
| 55–69 | Moderate | Noticeable variance or data gaps |
| 40–54 | Low | High variance or limited history |
| < 40 | Insufficient | Too little data or too much volatility |

### Inputs to the Score

1. **Monthly income amounts** (₹ INR, per month, for up to 6 months)
2. **Data completeness** (how many of the 6 window months have data)
3. **Income variance** (standard deviation relative to mean)
4. **Gap count** (number of zero-income or missing months)
5. **Recency weight** (more recent months can be weighted slightly higher)

### What GigScore Is Not

- It is not a **credit score**. Credwork does not make creditworthiness determinations.
- It is not a **fraud score**. Fraud detection is upstream; GigScore is only computed on documents that have already passed fraud checks.
- It is not **static**. Every certificate regeneration recalculates the GigScore from the latest data.

---

## 8. Colour System & Design Tokens

Credwork's visual identity uses the following design tokens across all product surfaces — web app, certificate PDFs, API documentation, and marketing materials.

| Token | Hex | Usage |
|---|---|---|
| `color-primary` | `#111827` | Charcoal Black — primary text, headings, certificate body |
| `color-secondary` | `#2563EB` | Electric Blue — CTAs, links, active states, chart highlights |
| `color-accent` | `#06B6D4` | Cyan — GigScore indicator, status badges, secondary charts |
| `color-background` | `#F4F6FA` | Off-White — app background, certificate background, card fills |

### Usage Guidelines

- **Charcoal Black (`#111827`)** is used for all primary text. Never use pure black (`#000000`) — it reads as harsh on the off-white background.
- **Electric Blue (`#2563EB`)** is the action colour. It should appear wherever the user can take an action (buttons, upload zones, links).
- **Cyan (`#06B6D4`)** is the data colour. Use it for GigScore rings, income trend charts, and any live data indicators.
- **Off-White (`#F4F6FA`)** is the background. Certificate PDFs should use this as the page background, not white — it reduces eye strain and visually distinguishes Credwork documents from generic PDFs.

---

## 9. Summary Mental Model

```
┌──────────────────────────────────────────────────────────────────┐
│                        CREDWORK SYSTEM                           │
│                                                                  │
│  INPUTS                  STATE                   OUTPUT          │
│  ─────────────────────   ───────────────────     ──────────────  │
│  Gig PDF uploads      →                       →                  │
│                           6-Month Rolling         Versioned      │
│  Razorpay payouts     →   Income Window       →   Certificate    │
│                           + GigScore             + GigScore      │
│  Salary updates       →                       →                  │
│                                                                  │
│  RULES                                                           │
│  ─────────────────────────────────────────────────────────────   │
│  • Newer data wins in conflicts (within fraud limits)            │
│  • Gaps are surfaced, never silently absorbed                    │
│  • Zero months are recorded, not excluded                        │
│  • Certificates only regenerate on >5% material change          │
│  • All versions are permanent — never deleted, never overwritten │
│  • Worker owns their income history across all households/jobs   │
└──────────────────────────────────────────────────────────────────┘
```

---

*Document maintained by the Credwork Product & Engineering team. All terminology (GigScore, ServiConnect, rolling window) is internal product language and should be used consistently across all written and verbal communications.*
