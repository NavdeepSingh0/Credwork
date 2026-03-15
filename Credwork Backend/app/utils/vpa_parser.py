import pdfplumber
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Optional


# ── Pattern Loading ──────────────────────────────────────────────────────────

GIG_PATTERNS_PATH = str(Path(__file__).parent.parent / "config" / "gig_patterns.json")
VPA_CONFIG_PATH = str(Path(__file__).parent.parent / "config" / "vpa_config.json")

_gig_patterns_cache: dict | None = None


def load_gig_patterns(config_path: str = GIG_PATTERNS_PATH) -> dict:
    """Load the gig_patterns.json dictionary. Cached after first call."""
    global _gig_patterns_cache
    if _gig_patterns_cache is not None:
        return _gig_patterns_cache
    with open(config_path) as f:
        _gig_patterns_cache = json.load(f)
    return _gig_patterns_cache


def load_vpa_lookup(config_path: str = VPA_CONFIG_PATH) -> dict:
    """Legacy: Returns a dict: vpa_string_lowercase → platform_name.
    Kept for backward compat; new code should use load_gig_patterns()."""
    with open(config_path) as f:
        config = json.load(f)
    lookup = {}
    for platform in config["platforms"]:
        for vpa in platform["vpas"]:
            lookup[vpa.lower()] = platform["name"]
    return lookup


# ── Platform Detection ───────────────────────────────────────────────────────

def detect_platform(description: str, vpa: Optional[str] = None,
                    patterns: dict | None = None) -> Optional[str]:
    """
    Return a platform slug like 'zomato', 'swiggy', 'rides', or None.
    Checks both VPA patterns and description keywords from gig_patterns.json.
    """
    if patterns is None:
        patterns = load_gig_patterns()

    d = (description or "").lower()
    v = (vpa or "").lower()

    # 1) VPA match
    for platform, cfg in patterns.items():
        for vpa_pattern in cfg.get("vpas", []):
            if v and vpa_pattern in v:
                return platform

    # 2) Description keyword match
    for platform, cfg in patterns.items():
        for kw in cfg.get("keywords", []):
            if kw in d:
                return platform

    return None


# ── Credit Extraction ────────────────────────────────────────────────────────

MONTH_MAP = {
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
    'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12',
    'january': '01', 'february': '02', 'march': '03', 'april': '04',
    'june': '06', 'july': '07', 'august': '08', 'september': '09',
    'october': '10', 'november': '11', 'december': '12',
}


def _parse_amount(cell_text: str) -> Optional[float]:
    """Parse a numeric amount from a cell, stripping commas and whitespace."""
    if not cell_text:
        return None
    cleaned = cell_text.strip().replace(',', '').replace('\n', '')
    # Remove Cr/Dr suffix
    cleaned = re.sub(r'\s*(Cr|Dr|CR|DR)\.?\s*$', '', cleaned, flags=re.IGNORECASE)
    try:
        val = float(cleaned)
        return val if val > 0 else None
    except (ValueError, TypeError):
        return None


def _parse_date(cell_text: str) -> Optional[str]:
    """
    Parse a date from a cell. Supports:
      - DD/MM/YYYY, DD-MM-YYYY
      - DD Mon YYYY, DD Mon\nYYYY (e.g. '13 Mar\\n2023')
    Returns YYYY-MM-DD string or None.
    """
    if not cell_text:
        return None
    text = cell_text.strip().replace('\n', ' ')

    # Format 1: DD/MM/YYYY or DD-MM-YYYY
    m = re.search(r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})', text)
    if m:
        day, month, year = m.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # Format 2: DD Mon YYYY (e.g. "13 Mar 2023")
    m = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', text)
    if m:
        day, month_str, year = m.groups()
        month_num = MONTH_MAP.get(month_str.lower())
        if month_num:
            return f"{year}-{month_num}-{day.zfill(2)}"

    return None


def _detect_columns(header_row: list) -> dict:
    """
    Detect column indices for Credit, Debit, Date, and Description
    from the header row of a bank statement table.
    Returns a dict with keys: credit_idx, debit_idx, date_idx, desc_idx (any may be None).
    """
    result = {'credit_idx': None, 'debit_idx': None, 'date_idx': None, 'desc_idx': None}
    credit_kw = ['credit', 'cr', 'deposit', 'credits']
    debit_kw = ['debit', 'dr', 'withdrawal', 'debits', 'withdrawals']
    date_kw = ['date', 'txn date', 'transaction date', 'value date']
    desc_kw = ['description', 'narration', 'particulars', 'details', 'remark']

    for idx, cell in enumerate(header_row):
        if not cell:
            continue
        cell_lower = cell.lower().replace('\n', ' ').strip()
        for kw in credit_kw:
            if kw in cell_lower:
                result['credit_idx'] = idx
                break
        for kw in debit_kw:
            if kw in cell_lower:
                result['debit_idx'] = idx
                break
        for kw in date_kw:
            if kw in cell_lower:
                result['date_idx'] = idx
                break
        for kw in desc_kw:
            if kw in cell_lower:
                result['desc_idx'] = idx
                break

    return result


def extract_all_credits(pdf_path: str) -> list:
    """
    Scans all pages and tables in a bank statement PDF.
    Returns a list of ALL credit transactions:
    [{ date, amount_inr, raw_description, platform (or None) }]

    Uses column-based extraction: detects header row to find Credit/Debit/Date
    columns, then reads each row using those column indices.
    Falls back to regex-based extraction if no header is found.
    """
    import logging
    logger = logging.getLogger(__name__)

    patterns = load_gig_patterns()
    transactions = []
    total_rows = 0
    skipped_rows = 0

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue

                # ─── Try to detect header row ─────────────────────────
                cols = _detect_columns(table[0])
                data_start = 1  # skip header

                # If first row isn't a header, try second row
                if cols['credit_idx'] is None and len(table) > 2:
                    cols = _detect_columns(table[1])
                    if cols['credit_idx'] is not None:
                        data_start = 2

                has_columns = cols['credit_idx'] is not None

                for row in table[data_start:]:
                    if not row:
                        continue
                    total_rows += 1

                    try:
                        row_text = ' '.join([str(cell) for cell in row if cell])

                        if has_columns:
                            # ── Column-based extraction ──────────────────
                            credit_cell = row[cols['credit_idx']] if cols['credit_idx'] is not None and cols['credit_idx'] < len(row) else None
                            debit_cell = row[cols['debit_idx']] if cols['debit_idx'] is not None and cols['debit_idx'] < len(row) else None

                            credit_amt = _parse_amount(str(credit_cell)) if credit_cell else None
                            debit_amt = _parse_amount(str(debit_cell)) if debit_cell else None

                            # We want credit rows: credit must be non-empty and debit should be empty/None
                            if not credit_amt:
                                skipped_rows += 1
                                continue
                            if debit_amt and debit_amt > 0:
                                # Both debit and credit populated — unusual, skip
                                skipped_rows += 1
                                continue

                            amount = credit_amt

                            # Get date from date column or from row text
                            date_str = None
                            if cols['date_idx'] is not None and cols['date_idx'] < len(row):
                                date_str = _parse_date(str(row[cols['date_idx']]))
                            if not date_str:
                                date_str = _parse_date(row_text)
                            if not date_str:
                                skipped_rows += 1
                                continue

                        else:
                            # ── Regex fallback (no header detected) ──────
                            amounts = re.findall(r'[\d,]+\.\d{2}', row_text)
                            if not amounts:
                                skipped_rows += 1
                                continue

                            is_cr_row = bool(re.search(r'\bCr\.?\b', row_text, re.IGNORECASE))

                            if len(amounts) >= 3:
                                amount_str = amounts[-2].replace(',', '')
                            elif len(amounts) == 2:
                                amount_str = amounts[0].replace(',', '') if is_cr_row else amounts[-2].replace(',', '')
                            else:
                                if not is_cr_row:
                                    skipped_rows += 1
                                    continue
                                amount_str = amounts[0].replace(',', '')

                            try:
                                amount = float(amount_str)
                                if amount <= 0:
                                    skipped_rows += 1
                                    continue
                            except ValueError:
                                skipped_rows += 1
                                continue

                            date_str = _parse_date(row_text)
                            if not date_str:
                                skipped_rows += 1
                                continue

                        # Sanity cap: reject > ₹50 lakh
                        if amount > 5000000:
                            skipped_rows += 1
                            continue

                        # Detect gig platform (or None for non-gig credits)
                        platform = detect_platform(row_text, patterns=patterns)

                        transactions.append({
                            "date": date_str,
                            "platform": platform,
                            "amount_inr": int(amount),
                            "raw_description": row_text[:200]
                        })

                    except Exception as e:
                        logger.warning(f"Skipped row on page {page_idx + 1}: {e}")
                        skipped_rows += 1
                        continue

    logger.info(f"PDF parsing complete: {total_rows} total rows, {len(transactions)} credits found, {skipped_rows} skipped")
    print(f"[vpa_parser] PDF parsing: {total_rows} total rows → {len(transactions)} credit transactions, {skipped_rows} skipped")
    return transactions


def classify_transactions(all_txns: list) -> tuple[list, list]:
    """
    Separates transactions into gig-platform transactions and all credit transactions.
    Returns: (gig_txns, credit_txns)
    - gig_txns: subset where platform is not None
    - credit_txns: ALL credit transactions (includes gig ones too)
    """
    gig_txns = []
    credit_txns = []

    for t in all_txns:
        credit_txns.append(t)
        if t.get("platform"):
            gig_txns.append(t)

    return gig_txns, credit_txns


# ── Legacy Wrapper ───────────────────────────────────────────────────────────

def extract_gig_income(pdf_path: str, config_path: str = VPA_CONFIG_PATH) -> list:
    """
    Legacy wrapper — extracts ONLY gig transactions (platform != None).
    Kept for backward compat with test_pipeline.py etc.
    """
    all_txns = extract_all_credits(pdf_path)
    gig_txns, _ = classify_transactions(all_txns)
    return gig_txns


# ── Aggregation ──────────────────────────────────────────────────────────────

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
        platform = txn.get("platform") or "Other"
        by_platform[month][platform] += txn["amount_inr"]

    monthly_totals = {
        month: sum(platforms.values())
        for month, platforms in by_platform.items()
    }

    return dict(by_platform), monthly_totals
