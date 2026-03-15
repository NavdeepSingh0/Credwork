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
    """
    if not monthly_totals:
        return {"score": 0, "label": "Insufficient", "inputs": {}}

    # Build the 6-month window (most recent 6 months)
    sorted_months = sorted(monthly_totals.keys(), reverse=True)
    window = sorted_months[:6]
    all_amounts = [monthly_totals.get(m, 0) for m in window]

    months_with_income = len([a for a in all_amounts if a > 0])
    months_with_zero = len(all_amounts) - months_with_income

    if months_with_income == 0:
        return {"score": 0, "label": "Insufficient", "inputs": {}}

    mean_income = statistics.mean(all_amounts)
    std_dev = statistics.stdev(all_amounts) if len(all_amounts) > 1 else 0
    cv = std_dev / mean_income if mean_income > 0 else 1.0

    # Component A: Consistency (0–100, inverse of CV)
    consistency_score = max(0, 100 - (cv * 100))

    # Component B: Completeness (0–100)
    completeness_score = (months_with_income / 6) * 100

    # Component C: Gap penalty
    gap_penalty = months_with_zero * 10

    # Component D: Recency bonus
    recency_bonus = 0
    if len(all_amounts) >= 6:
        recent_mean = statistics.mean(all_amounts[:3])
        older_mean = statistics.mean(all_amounts[3:])
        if older_mean > 0 and recent_mean >= older_mean * 0.9:
            recency_bonus = 5

    # Combine with weights
    raw_score = (
        (consistency_score * 0.50) +
        (completeness_score * 0.35) +
        recency_bonus
    ) - gap_penalty

    final_score = max(0, min(100, round(raw_score)))

    # Assign label
    label = "Insufficient"
    for threshold, lbl in LABELS:
        if final_score >= threshold:
            label = lbl
            break

    return {
        "score": final_score,
        "label": label,
        "inputs": {
            "months_in_window": len(window),
            "months_with_income": months_with_income,
            "mean_income_inr": round(mean_income),
            "coefficient_of_variation": round(cv, 3),
            "consistency_score": round(consistency_score),
            "completeness_score": round(completeness_score),
            "gap_penalty": gap_penalty,
            "recency_bonus": recency_bonus
        }
    }
