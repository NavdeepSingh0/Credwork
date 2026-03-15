"""
test_two_mode.py — Tests the two-mode detection logic:
  1. Gig statement → mode="gig", platforms detected
  2. Generic salary statement → mode="generic", no platforms
  3. Empty/invalid PDF → mode="invalid" (no credits)

Run: python test_two_mode.py
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

os.makedirs("test_output", exist_ok=True)


# ── Test 1: Gig statement (Swiggy/Zomato/Rapido credits) ────────────────────

def generate_gig_statement(path):
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>HDFC BANK — Account Statement</b>", styles["Heading1"]),
        Spacer(1, 10),
    ]
    headers = ["Date", "Description", "Debit (₹)", "Credit (₹)", "Balance (₹)"]
    rows = [
        ["01/10/2024", "UPI-swiggy@icici-Swiggy Technologies", "", "4,200.00", "12,400.00"],
        ["05/10/2024", "UPI-zomato@icici-Zomato Ltd", "", "3,800.00", "16,200.00"],
        ["10/10/2024", "NEFT-Roppen Transportation-rapido", "", "3,200.00", "19,400.00"],
        ["01/11/2024", "UPI-swiggy@ybl-Swiggy Technologies", "", "4,500.00", "23,900.00"],
        ["05/11/2024", "UPI-zomato@hdfcbank-Zomato Ltd", "", "4,200.00", "28,100.00"],
        ["01/12/2024", "UPI-blinkit@icici-Blinkit Commerce", "", "2,800.00", "30,900.00"],
    ]
    table = Table([headers] + rows, colWidths=[2.5*cm, 7*cm, 2*cm, 2.2*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    doc.build(story)


# ── Test 2: Generic salary statement (NEFT transfers, no gig keywords) ───────

def generate_generic_statement(path):
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>SBI — Savings Account Statement</b>", styles["Heading1"]),
        Spacer(1, 10),
    ]
    headers = ["Date", "Description", "Debit (₹)", "Credit (₹)", "Balance (₹)"]
    rows = [
        ["01/10/2024", "NEFT-ACME Corp-Oct Salary", "", "35,000.00", "42,000.00"],
        ["15/10/2024", "ATM Withdrawal Delhi", "5,000.00", "", "37,000.00"],
        ["01/11/2024", "NEFT-ACME Corp-Nov Salary", "", "35,000.00", "72,000.00"],
        ["10/11/2024", "UPI-Electricity Bill Payment", "2,500.00", "", "69,500.00"],
        ["01/12/2024", "NEFT-ACME Corp-Dec Salary", "", "36,000.00", "95,500.00"],  # credit > 100k check: balance is fine
        ["15/12/2024", "NEFT-Family Transfer", "", "10,000.00", "95,500.00"],
    ]
    table = Table([headers] + rows, colWidths=[2.5*cm, 7*cm, 2*cm, 2.2*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    doc.build(story)


# ── Test 3: Empty / invalid PDF (no transactions table) ─────────────────────

def generate_empty_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("<b>This is not a bank statement</b>", styles["Heading1"]),
        Paragraph("Just some random text with no transaction data.", styles["Normal"]),
    ]
    doc.build(story)


# ── Run all tests ────────────────────────────────────────────────────────────

def run_tests():
    from app.utils.vpa_parser import extract_all_credits, classify_transactions, aggregate_by_month

    print("=" * 60)
    print("TWO-MODE DETECTION TESTS")
    print("=" * 60)

    passed = 0
    failed = 0

    # ── TEST 1: Gig statement ──
    print("\n[TEST 1] Gig worker bank statement")
    gig_path = "test_output/test_gig_statement.pdf"
    generate_gig_statement(gig_path)

    all_txns = extract_all_credits(gig_path)
    gig_txns, credit_txns = classify_transactions(all_txns)

    if gig_txns:
        mode = "gig"
    elif credit_txns:
        mode = "generic"
    else:
        mode = "invalid"

    platforms = sorted(set(t["platform"] for t in gig_txns if t.get("platform")))
    print(f"  All credits:     {len(credit_txns)}")
    print(f"  Gig credits:     {len(gig_txns)}")
    print(f"  Mode:            {mode}")
    print(f"  Platforms:       {platforms}")

    if mode == "gig" and len(gig_txns) > 0 and len(platforms) > 0:
        print("  ✅ PASS")
        passed += 1
    else:
        print("  ❌ FAIL — expected mode='gig' with platforms detected")
        failed += 1

    # ── TEST 2: Generic salary statement ──
    print("\n[TEST 2] Generic salary bank statement (no gig platforms)")
    generic_path = "test_output/test_generic_statement.pdf"
    generate_generic_statement(generic_path)

    all_txns = extract_all_credits(generic_path)
    gig_txns, credit_txns = classify_transactions(all_txns)

    if gig_txns:
        mode = "gig"
    elif credit_txns:
        mode = "generic"
    else:
        mode = "invalid"

    print(f"  All credits:     {len(credit_txns)}")
    print(f"  Gig credits:     {len(gig_txns)}")
    print(f"  Mode:            {mode}")

    if mode == "generic" and len(gig_txns) == 0 and len(credit_txns) > 0:
        print("  ✅ PASS")
        passed += 1
    else:
        print(f"  ❌ FAIL — expected mode='generic' with 0 gig txns and >0 credit txns")
        failed += 1

    # Show the credit transactions for debugging
    if credit_txns:
        by_platform, monthly_totals = aggregate_by_month(credit_txns)
        print(f"  Monthly totals:  {monthly_totals}")

    # ── TEST 3: Empty PDF (no transactions) ──
    print("\n[TEST 3] Empty / invalid PDF (no transaction table)")
    empty_path = "test_output/test_empty.pdf"
    generate_empty_pdf(empty_path)

    all_txns = extract_all_credits(empty_path)
    gig_txns, credit_txns = classify_transactions(all_txns)

    if gig_txns:
        mode = "gig"
    elif credit_txns:
        mode = "generic"
    else:
        mode = "invalid"

    print(f"  All credits:     {len(credit_txns)}")
    print(f"  Gig credits:     {len(gig_txns)}")
    print(f"  Mode:            {mode}")

    if mode == "invalid":
        print("  ✅ PASS")
        passed += 1
    else:
        print(f"  ❌ FAIL — expected mode='invalid'")
        failed += 1

    # ── Summary ──
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
