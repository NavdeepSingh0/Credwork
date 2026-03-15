import statistics
from typing import Optional


LABELS = [
    (85, "Excellent"),
    (70, "Good"),
    (55, "Moderate"),
    (40, "Low"),
    (0,  "Insufficient")
]


def calculate_gigscore(monthly_totals: dict) -> dict:
    """
    monthly_totals: { "2025-01": 21000, "2025-02": 18000, ... }
    Returns: { score, label, inputs }

    Scoring Rules:
    - Less than 3 months of data → capped at "Low" (max 39)
    - 3–5 months → max "Good" (capped at 79)
    - 6+ months → can reach "Excellent" (up to 100)
    - Months with zero income within the window are penalized
    """
    if not monthly_totals:
        return {"score": 0, "label": "Insufficient", "inputs": {}}

    # Use up to 6 most recent months
    sorted_months = sorted(monthly_totals.keys(), reverse=True)
    window = sorted_months[:6]
    all_amounts = [monthly_totals.get(m, 0) for m in window]
    window_size = len(window)

    months_with_income = len([a for a in all_amounts if a > 0])
    months_with_zero = window_size - months_with_income

    if months_with_income == 0:
        return {"score": 0, "label": "Insufficient", "inputs": {}}

    mean_income = statistics.mean(all_amounts)
    std_dev = statistics.stdev(all_amounts) if len(all_amounts) > 1 else 0
    cv = std_dev / mean_income if mean_income > 0 else 1.0

    # ── Component A: Consistency (0–100, inverse of coefficient of variation)
    consistency_score = max(0, 100 - (cv * 100))

    # ── Component B: Data depth — how many months available (0–100)
    # 1 month → 16.7, 2 → 33.3, 3 → 50, 4 → 66.7, 5 → 83.3, 6 → 100
    depth_score = (months_with_income / 6) * 100

    # ── Component C: Gap penalty — zero-income months in the window
    gap_penalty = months_with_zero * 8

    # ── Component D: Recency bonus (only for 6-month windows)
    recency_bonus = 0
    if window_size >= 6:
        recent_mean = statistics.mean(all_amounts[:3])
        older_mean = statistics.mean(all_amounts[3:])
        if older_mean > 0 and recent_mean >= older_mean * 0.9:
            recency_bonus = 5

    # ── Combine with weights
    raw_score = (
        (consistency_score * 0.40) +
        (depth_score * 0.45) +
        recency_bonus
    ) - gap_penalty

    # ── Apply hard caps based on months of data ──
    # Less than 3 months: cap at 39 (Low)
    # 3–5 months: cap at 79 (Good max)
    # 6+ months: no cap
    if months_with_income < 3:
        cap = 39  # "Low" max — need at least 3 months for decent score
    elif months_with_income < 6:
        cap = 79  # "Good" max — need 6+ months for Excellent
    else:
        cap = 100

    final_score = max(0, min(cap, round(raw_score)))

    # ── Assign label
    label = "Insufficient"
    for threshold, lbl in LABELS:
        if final_score >= threshold:
            label = lbl
            break

    return {
        "score": final_score,
        "label": label,
        "inputs": {
            "months_in_window": window_size,
            "months_with_income": months_with_income,
            "mean_income_inr": round(mean_income),
            "coefficient_of_variation": round(cv, 3),
            "consistency_score": round(consistency_score),
            "depth_score": round(depth_score),
            "gap_penalty": gap_penalty,
            "recency_bonus": recency_bonus,
            "cap_applied": cap,
        }
    }
