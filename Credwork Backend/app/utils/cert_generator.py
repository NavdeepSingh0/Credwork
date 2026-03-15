import os
import io
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm
from app.config.database import get_supabase
from app.config.settings import settings
from supabase import create_client

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


async def generate_certificate(worker_id: str, gigscore_result: dict, db, mode: str = "gig") -> str | None:
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

    # ── Build PDF into memory buffer ─────────────────────────
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    story = []

    # Header — changes based on mode
    cert_title = "Gig Income Verification Certificate" if mode == "gig" else "Cash-Flow Income Certificate"
    score_label_text = "GigScore" if mode == "gig" else "Cash-Flow Score"

    story.append(Paragraph(
        "<font color='#10B981'><b>Credwork</b></font>",
        ParagraphStyle("brand", fontSize=28, spaceAfter=4)
    ))
    story.append(Paragraph(
        cert_title,
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

    # Score box
    score_label_color = "#10B981" if gigscore_result["score"] >= 70 else "#F59E0B" if gigscore_result["score"] >= 55 else "#EF4444"
    story.append(Table(
        [[
            f"{score_label_text}: {gigscore_result['score']}/100",
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

    # Generic mode note
    if mode == "generic":
        story.append(Paragraph(
            "<i>No known gig platform payouts were detected. This certificate is based on all credited income only.</i>",
            ParagraphStyle("generic_note", fontSize=9, textColor=DARK_GREY, spaceAfter=12)
        ))

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

    # ── Upload to Supabase Storage ─────────────────────────────
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    public_url = _save_certificate_to_storage(pdf_bytes, cert_id)

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
        "pdf_url": public_url,
        "mode": mode
    }).execute()

    return cert_id


def _save_certificate_to_storage(pdf_bytes: bytes, cert_id: str) -> str:
    """
    Uploads certificate PDF to Supabase Storage.
    Returns the public URL.
    """
    storage_client = create_client(
        settings.supabase_url,
        settings.supabase_service_key
    )
    file_path = f"certificates/{cert_id}.pdf"

    storage_client.storage.from_("certificates").upload(
        path=file_path,
        file=pdf_bytes,
        file_options={"content-type": "application/pdf", "upsert": "true"}
    )

    public_url = storage_client.storage.from_("certificates").get_public_url(file_path)
    return public_url
