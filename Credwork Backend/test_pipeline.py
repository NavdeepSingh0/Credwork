"""
test_pipeline.py — Generates a synthetic gig worker bank statement PDF
and runs the complete verification pipeline on it.

Run: python test_pipeline.py
"""

import os
import sys
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# ── Step 1: Generate a synthetic HDFC-style bank statement ──────────────────

def generate_synthetic_statement(output_path: str):
    """
    Creates a PDF that looks like an HDFC bank statement with UPI credits
    from Swiggy, Zomato, and Rapido — the kind a gig worker would have.
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=1.5*cm, leftMargin=1.5*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    # Bank header
    story.append(Paragraph("<b>HDFC BANK</b>", styles["Heading1"]))
    story.append(Paragraph("Account Statement", styles["Heading2"]))
    story.append(Paragraph("Account Number: XXXX XXXX 4128 | Period: Oct 2024 – Mar 2025", styles["Normal"]))
    story.append(Paragraph("Account Holder: Raju Kumar | Branch: Mumbai Central", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Transaction table — mimics real HDFC statement layout
    # Columns: Date | Description | Ref No | Debit | Credit | Balance
    headers = ["Date", "Description", "Ref No", "Debit (₹)", "Credit (₹)", "Balance (₹)"]

    transactions = [
        # Oct 2024
        ["01/10/2024", "UPI-swiggy@icici-Swiggy Technologies", "TXN2410010001", "", "4,200.00", "12,400.00"],
        ["05/10/2024", "UPI-zomato@icici-Zomato Ltd", "TXN2410050002", "", "3,800.00", "16,200.00"],
        ["10/10/2024", "UPI-rapido@icici-Roppen Transportation", "TXN2410100003", "", "3,200.00", "19,400.00"],
        ["15/10/2024", "ATM WDL MUMBAI", "TXN2410150004", "500.00", "", "18,900.00"],
        ["20/10/2024", "UPI-swiggy@icici-Swiggy Technologies", "TXN2410200005", "", "3,800.00", "22,700.00"],

        # Nov 2024
        ["02/11/2024", "UPI-swiggy@ybl-Swiggy Technologies", "TXN2411020006", "", "4,500.00", "27,200.00"],
        ["08/11/2024", "UPI-zomato@icici-Zomato Ltd", "TXN2411080007", "", "4,200.00", "31,400.00"],
        ["15/11/2024", "UPI-rapido@ybl-Roppen Transportation", "TXN2411150008", "", "3,600.00", "35,000.00"],
        ["22/11/2024", "UPI-swiggy@icici-Swiggy Technologies", "TXN2411220009", "", "3,900.00", "38,900.00"],

        # Dec 2024
        ["03/12/2024", "UPI-swiggy@icici-Swiggy Technologies", "TXN2412030010", "", "4,100.00", "43,000.00"],
        ["10/12/2024", "UPI-blinkit@icici-Blinkit Commerce", "TXN2412100011", "", "2,800.00", "45,800.00"],
        ["18/12/2024", "UPI-zomato@hdfcbank-Zomato Ltd", "TXN2412180012", "", "3,500.00", "49,300.00"],
        ["25/12/2024", "ATM WDL MUMBAI", "TXN2412250013", "2,000.00", "", "47,300.00"],

        # Jan 2025
        ["04/01/2025", "UPI-swiggy@icici-Swiggy Technologies", "TXN2501040014", "", "4,800.00", "52,100.00"],
        ["10/01/2025", "UPI-zomato@icici-Zomato Ltd", "TXN2501100015", "", "3,900.00", "56,000.00"],
        ["17/01/2025", "UPI-rapido@icici-Roppen Transportation", "TXN2501170016", "", "3,300.00", "59,300.00"],
        ["24/01/2025", "UPI-swiggy@ybl-Swiggy Technologies", "TXN2501240017", "", "4,200.00", "63,500.00"],

        # Feb 2025
        ["03/02/2025", "UPI-swiggy@icici-Swiggy Technologies", "TXN2502030018", "", "4,400.00", "67,900.00"],
        ["10/02/2025", "UPI-zomato@kotak-Zomato Ltd", "TXN2502100019", "", "3,700.00", "71,600.00"],
        ["18/02/2025", "UPI-blinkit@icici-Blinkit Commerce", "TXN2502180020", "", "2,900.00", "74,500.00"],
        ["25/02/2025", "ATM WDL MUMBAI", "TXN2502250021", "1,000.00", "", "73,500.00"],

        # Mar 2025
        ["05/03/2025", "UPI-swiggy@icici-Swiggy Technologies", "TXN2503050022", "", "4,600.00", "78,100.00"],
        ["12/03/2025", "UPI-zomato@icici-Zomato Ltd", "TXN2503120023", "", "3,800.00", "81,900.00"],
        ["19/03/2025", "UPI-rapido@ybl-Roppen Transportation", "TXN2503190024", "", "3,100.00", "85,000.00"],
    ]

    table_data = [headers] + transactions

    table = Table(table_data, colWidths=[2.5*cm, 6*cm, 3.5*cm, 2*cm, 2.2*cm, 2.2*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("This is a computer-generated statement. No signature required.", styles["Normal"]))

    doc.build(story)
    print(f"✅ Synthetic bank statement created: {output_path}")


# ── Step 2: Run the full pipeline ────────────────────────────────────────────

def run_pipeline(pdf_path: str):
    print("\n" + "="*60)
    print("CREDWORK VERIFICATION PIPELINE TEST")
    print("="*60)

    # --- Layer 1: Fraud Check ---
    print("\n[LAYER 1] Fraud Check (pikepdf)")
    from app.utils.fraud import run_fraud_checks
    fraud_result = run_fraud_checks(pdf_path)
    print(f"  Metadata check:    {fraud_result['metadata_check']}")
    print(f"  Font check:        {fraud_result['font_check']}")
    print(f"  Edit history:      {fraud_result['edit_history_check']}")
    print(f"  PASSED:            {fraud_result['passed']}")
    if not fraud_result['passed']:
        print(f"  ❌ REASON: {fraud_result['reason']}")
        print("\n⚠️  Fraud check failed — pipeline would stop here in production.")
        print("   This is expected with synthetic PDFs (creator = ReportLab, not a bank).")
        print("   Continuing anyway to test VPA extraction...\n")
    else:
        print("  ✅ Fraud check passed!")

    # --- Layer 2: VPA Extraction ---
    print("\n[LAYER 2] VPA / Income Extraction (pdfplumber)")
    from app.utils.vpa_parser import extract_gig_income, aggregate_by_month
    config_path = "app/config/vpa_config.json"
    transactions = extract_gig_income(pdf_path, config_path)

    if not transactions:
        print("  ❌ No gig transactions found!")
        print("  This means pdfplumber couldn't match VPA strings in the PDF tables.")
    else:
        print(f"  ✅ Found {len(transactions)} gig transactions:")
        for t in transactions:
            print(f"     {t['date']}  {t['platform']:<15}  ₹{t['amount_inr']:,}")

        by_platform, monthly_totals = aggregate_by_month(transactions)
        print(f"\n  Monthly totals:")
        for month in sorted(monthly_totals.keys()):
            print(f"     {month}:  ₹{monthly_totals[month]:,}")

        # --- Layer 3: GigScore ---
        print("\n[LAYER 3] GigScore Calculation")
        from app.utils.gigscore import calculate_gigscore
        gigscore = calculate_gigscore(monthly_totals)
        print(f"  Score:  {gigscore['score']}/100  ({gigscore['label']})")
        print(f"  Inputs: {gigscore['inputs']}")

        # --- Layer 4: ML Anomaly Detection ---
        print("\n[LAYER 4] ML Anomaly Detection (IsolationForest)")
        from app.ml.anomaly_detector import detect_income_anomalies, get_anomaly_severity
        amounts = [monthly_totals.get(m, 0) for m in sorted(monthly_totals.keys())]
        anomaly = detect_income_anomalies(amounts)
        severity = get_anomaly_severity(anomaly)
        print(f"  Anomaly detected:  {anomaly['anomaly_detected']}")
        print(f"  Severity:          {severity}")
        print(f"  Confidence:        {anomaly['model_confidence']}")
        if anomaly['reason']:
            print(f"  Reason:            {anomaly['reason']}")
        else:
            print(f"  ✅ No anomalies detected — income pattern looks normal.")

    print("\n" + "="*60)
    print("PIPELINE TEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    os.makedirs("test_output", exist_ok=True)
    pdf_path = "test_output/synthetic_statement.pdf"

    generate_synthetic_statement(pdf_path)
    run_pipeline(pdf_path)
