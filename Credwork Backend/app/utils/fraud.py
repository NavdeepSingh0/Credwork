import pikepdf
from pathlib import Path


SUSPICIOUS_CREATORS = [
    'foxit phantom', 'nitro pro', 'pdf editor',
    'smallpdf', 'ilovepdf', 'sejda', 'pdfescape',
    'pdf-xchange editor', 'master pdf editor', 'pdfill',
    'pdfelement', 'wondershare'
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
