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

                    # Extract all amounts — matches formats: 1,234.56 or 1234.56
                    amounts = re.findall(r'[\d,]+\.\d{2}', row_text)
                    if not amounts:
                        continue

                    # ─── FIX: Take the correct credit column ───────────────────
                    # Bank statement columns are typically:
                    #   Date | Description | Debit | Credit | Balance
                    # amounts[-1] = Balance (running total — WRONG)
                    # amounts[-2] = Credit amount (CORRECT, when debit is empty)
                    # If there's only one amount, that's the credit.
                    if len(amounts) >= 2:
                        # Take second-to-last (credit column); last is balance
                        amount_str = amounts[-2].replace(',', '')
                    else:
                        amount_str = amounts[0].replace(',', '')

                    try:
                        amount = float(amount_str)
                        # Sanity check: UPI gig payments are typically ₹500–₹50,000
                        # Reject amounts that look like balances (>100,000) or are zero/negative
                        if amount <= 0 or amount > 100000:
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
