# Workli Bank Statement Verification – Final Agreed Solution

_Last updated: 15 March 2026_

This document describes the **final, non‑gimmicky solution** for Workli’s bank‑statement based income verification, including:

- Behaviour for **any Indian bank statement** (not just gig workers)
- A **two‑mode certificate model** (Gig Income vs Generic Cash‑Flow)
- A realistic, extensible **gig pattern dictionary** (keywords & VPAs)
- How backend and frontend should use these concepts

The goal is:

1. Judges can upload **any PDF bank statement** even when we are not present, and the app still shows a sensible certificate instead of an error.
2. When we are present, we can demo **true gig‑income detection and verification** using realistic patterns.

---

## 1. High‑Level Behaviour

### 1.1 Two Certificate Modes

Instead of a binary **"gig worker or error"**, Workli now has **two valid modes**, plus a true error state:

1. **Gig Income Certificate (mode = `gig`)**  
   Used when we detect **any transactions that look like payouts from gig / quick‑commerce / ride‑hailing platforms** (Swiggy, Zomato, Blinkit, etc.).

2. **Cash‑Flow Income Certificate (mode = `generic`)**  
   Used when **no gig patterns are found** but the statement clearly shows other regular credits (salary, transfers, etc.). This is still valuable for lenders as a cash‑flow–based income view.

3. **Error (mode = `invalid`)**  
   Only used when:
   - The PDF cannot be parsed as a statement at all (no transaction table), or
   - There are **no credit transactions** in the period (empty/invalid input).

### 1.2 Why this is realistic

- Real income‑verification tools (Perfios, Ocrolus, etc.) always build a **transaction‑level classifier** on top of bank statements, and then aggregate by category (salary, gig income, transfers, etc.).
- Our approach mirrors that:
  - We extract **all transactions**.
  - We classify credits into **`gig` vs `non_gig`** using a dictionary of patterns.
  - We aggregate accordingly and produce a certificate that is **never just "mock"**.

---

## 2. Data Flow Overview

1. **PDF Upload**  
   User uploads an Indian bank statement PDF (SBI, HDFC, ICICI, etc.).

2. **Parsing Layer**  
   - Libraries: `PyMuPDF` / `pdfplumber` for text extraction, plus Tesseract OCR fallback for scanned PDFs.
   - Output: a list of transactions with fields:
     ```json
     {
       "date": "2024-04-01",
       "description": "BY TRANSFER NEFT*ZOMA0001*ZOMATO MEDIA/Apr W1 Earning",
       "debit": 0,
       "credit": 3840.00,
       "balance": 11932.35,
       "vpa": null   // if we can parse a UPI VPA, else null
     }
     ```

3. **Fraud & Integrity Checks**  
   - `pdfid` and `pikepdf` for metadata and structure sanity.
   - Basic structure checks (pages > 1, table present, etc.).
   - These populate a `fraud_checklist` that is shown transparently in the UI.

4. **Classification Layer**  
   - Uses **`gig_patterns.json`** (see Section 4) to decide which credit transactions are gig‑related.
   - Computes statistics separately for **gig income** (`gig_txns`) and **all credits** (`credit_txns`).

5. **Mode Decision**  
   - If `gig_txns` is non‑empty: **`mode = "gig"`**.  
   - Else if `credit_txns` is non‑empty: **`mode = "generic"`**.  
   - Else: **`mode = "invalid"`** → show proper error.

6. **Certificate Generation**  
   - Same pipeline (ReportLab PDF) for both modes, with different framing and flags.

---

## 3. Backend Behaviour in Detail

### 3.1 Transaction Classification

**Input:** `all_txns` = list of parsed transactions.

```python
from typing import Optional

# patterns loaded from gig_patterns.json (see section 4)
GIG_PATTERNS: dict = load_patterns()


def detect_platform(description: str, vpa: Optional[str]) -> Optional[str]:
    """Return a platform slug like 'zomato', 'blinkit', 'swiggy', or None."""
    d = (description or "").lower()
    v = (vpa or "").lower()

    # 1) Exact or partial VPA match
    for platform, cfg in GIG_PATTERNS.items():
        for vpa_pattern in cfg.get("vpas", []):
            if v and vpa_pattern in v:
                return platform

    # 2) Description keyword match
    for platform, cfg in GIG_PATTERNS.items():
        for kw in cfg.get("keywords", []):
            if kw in d:
                return platform

    return None


def classify_transactions(all_txns):
    gig_txns = []
    credit_txns = []

    for t in all_txns:
        if t.credit_amount <= 0:
            continue

        credit_txns.append(t)
        platform = detect_platform(t.description, t.vpa)
        if platform:
            t.platform = platform
            gig_txns.append(t)

    return gig_txns, credit_txns
```

This logic:

- Treats **only credits** as potential income.
- Relies on both **VPA patterns** (if available) and **description keywords**.
- Works on:
  - Mock SBI gig statement (Zomato / Blinkit NEFT credits).
  - Real statements where narration includes `"ZOMATO MEDIA"`, `"BLINKIT GROFERS"`, `"SWIGGY"`, etc.

### 3.2 Mode Selection and Metrics

```python
def analyze_income(all_txns, fraud_checklist):
    gig_txns, credit_txns = classify_transactions(all_txns)

    if gig_txns:
        mode = "gig"
        income_src = gig_txns
    elif credit_txns:
        mode = "generic"
        income_src = credit_txns
    else:
        return {
            "status": "error",
            "mode": "invalid",
            "reason": "no_credit_transactions",
            "fraud_checklist": fraud_checklist,
        }

    # Aggregate statistics
    monthly_avg = compute_monthly_average(income_src)
    stability_score = compute_stability_score(income_src)
    platforms = sorted({getattr(t, "platform", None) for t in gig_txns if getattr(t, "platform", None)})

    return {
        "status": "success",
        "mode": mode,
        "monthly_avg": monthly_avg,
        "stability_score": stability_score,
        "platforms_detected": platforms,
        "fraud_checklist": fraud_checklist,
    }
```

### 3.3 API Response Shape

**Endpoint:** `POST /verification/gig/upload`

Successful response:

```json
{
  "status": "success",
  "mode": "gig",                // or "generic"
  "monthly_avg": 28400,
  "stability_score": 0.92,
  "platforms_detected": ["zomato", "blinkit"],
  "fraud_checklist": {
    "pdf_metadata": "PASS",
    "structure": "PASS",
    "tampering": "PASS",
    "income_realism": "PASS"
  },
  "certificate_url": "/cert/verif_xyz789.pdf"
}
```

Error response (true invalid case):

```json
{
  "status": "error",
  "mode": "invalid",
  "reason": "no_credit_transactions",
  "fraud_checklist": {
    "pdf_metadata": "PASS",
    "structure": "PASS",
    "tampering": "PASS"
  }
}
```

Front‑end logic:

- If `status === "success"`:
  - If `mode === "gig"` → show **Gig Income Certificate** UI (with detected platforms badges).
  - If `mode === "generic"` → show **Cash‑Flow Income Certificate** UI with a yellow banner:  
    _"No known gig platforms found. This certificate is based on all credited income only."_
- If `status === "error"` and `mode === "invalid"` → show the existing error screen.

---

## 4. Realistic Gig Pattern Dictionary (Starter Set)

The pattern dictionary lives in **`config/gig_patterns.json`**. It drives classification and is meant to be **extended over time**.

### 4.1 Design

- Top‑level keys are **platform slugs** (`"zomato"`, `"blinkit"`, `"swiggy"`, `"rides"`, etc.).
- Each platform has two lists:
  - `"vpas"`: known or partial VPA patterns (if any).
  - `"keywords"`: substrings to search for in the Description / Narration.

### 4.2 Starter JSON

```json
{
  "zomato": {
    "vpas": [
      "zomato@upi"
    ],
    "keywords": [
      "zomato media",
      "zomato private ltd",
      "zomato w1 earning",
      "zomato w2 earning",
      "zomato w3 earning",
      "zomato w4 earning",
      "zoma000"          
    ]
  },

  "blinkit": {
    "vpas": [],
    "keywords": [
      "blinkit",
      "blinkit grofers",
      "grofers",
      "blink000"         
    ]
  },

  "swiggy": {
    "vpas": [
      "swiggy@icici",
      "swiggy@yesbank"
    ],
    "keywords": [
      "swiggy",
      "swiggy food",
      "swiggy instamart"
    ]
  },

  "rides": {
    "vpas": [],
    "keywords": [
      "uber india",
      "ola cabs",
      "rapido"
    ]
  },

  "other_gig": {
    "vpas": [],
    "keywords": [
      "zepto",
      "bigbasket",
      "d-mart",
      "dmart"
    ]
  }
}
```

### 4.3 How to Extend Safely

- As you see real statements from workers, just append **new observed substrings** into the appropriate `keywords` list.
- For VPAs, you **never need to guess full VPAs**; partial patterns like `"swiggy"` inside a VPA are enough.
- Because we always require **credit transactions**, false positives from pure consumer spends (e.g. ordering food FROM Swiggy) are limited; but you can:
  - Restrict gig detection to **NEFT/IMPS credits** or UPI _incoming_ transfers, not debits.
  - Optionally require a **minimum size and repetition** (e.g. at least 2–3 credits from that pattern in a month) to treat it as income.

---

## 5. Front‑End UX Expectations

### 5.1 Upload Result States

For any uploaded statement, the user sees one of three clear outcomes:

1. **Gig Income Certificate**  
   - Badge: `Gig Income Verified`  
   - Shows: platforms detected, gig monthly average, gig stability score.

2. **Cash‑Flow Income Certificate**  
   - Badge: `Cash‑Flow Income Summary`  
   - Info banner:  
     _"We didn\'t find payouts from known platforms like Swiggy or Zomato. This certificate is based on all credited income only."_

3. **Upload Error**  
   - Message:  
     _"We couldn't read this as a bank statement. Please upload a PDF statement downloaded from your bank's website or app."_

### 5.2 Fraud Checklist UI

The checklist remains the same for both modes, e.g.:

- PDF metadata: PASS / FAIL
- Structure: PASS / WARN
- Tampering heuristics: PASS / WARN
- Platform match: `"Swiggy, Zomato"` / `"None detected"`

This makes the demo feel **credible** to judges and to any fintech mentor.

---

## 6. Demo Strategy Using This Design

1. **Judge alone (no team present)**  
   - They upload any SBI/HDFC/ICICI statement → always get either Gig or Generic certificate.  
   - No dependency on special mock PDFs.

2. **You present live**  
   Use three PDFs:
   - A normal salary/transfer statement → Generic mode.  
   - Your mock SBI gig statement (with Zomato / Blinkit earnings) → Gig mode with platforms.  
   - A garbage/non‑statement PDF → Error mode with helpful guidance.

This demonstrates:

- Robust parsing and fraud checks.
- Realistic gig detection using brand patterns.
- Sensible fallback behaviour for all other cases.

---

## 7. Files for the Backend/Frontend Team

- `config/gig_patterns.json` – pattern dictionary (starter version above).
- `vpa_parser.py` – parsing + `detect_platform()` + `classify_transactions()`.
- `income_analysis.py` – `analyze_income()` + metrics.
- `cert_generator.py` – shared PDF generator for both modes.

Give this markdown file + `gig_patterns.json` to antigravity and the backend dev so everyone is aligned on the **same behaviour and data structures**.
