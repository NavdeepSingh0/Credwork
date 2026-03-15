from typing import List, Dict, Any


def detect_income_anomalies(monthly_amounts: List[float]) -> Dict[str, Any]:
    """
    Uses IsolationForest (unsupervised ML) to detect anomalous months
    in a worker's income history.

    IsolationForest works by building random decision trees and measuring
    how quickly each data point can be "isolated". Points that are isolated
    quickly (few splits needed) are anomalies — they are far from the cluster.

    Args:
        monthly_amounts: List of monthly income totals in INR.
                         Must be in chronological order.
                         Zero-income months must be included (not excluded).

    Returns:
        Dict containing:
          - anomaly_detected: bool — True if any month is anomalous
          - anomalous_indices: List[int] — indices of anomalous months
          - anomaly_scores: List[float] — anomaly score per month (-1 to 0,
                            lower = more anomalous)
          - model_confidence: float — how reliable this detection is
                              (based on sample size, 0 to 1)
          - reason: str | None — plain language explanation if anomaly found
    """

    # Minimum 3 data points required for meaningful anomaly detection
    if len(monthly_amounts) < 3:
        return {
            "anomaly_detected": False,
            "anomalous_indices": [],
            "anomaly_scores": [],
            "model_confidence": 0.0,
            "reason": None,
            "skipped": True,
            "skip_reason": "Insufficient data — need at least 3 months"
        }

    try:
        import numpy as np
        from sklearn.ensemble import IsolationForest
    except Exception:
        return {
            "anomaly_detected": False,
            "anomalous_indices": [],
            "anomaly_scores": [],
            "model_confidence": 0.0,
            "reason": None,
            "skipped": True,
            "skip_reason": "ML anomaly detection unavailable in this environment"
        }

    amounts = np.array(monthly_amounts, dtype=float).reshape(-1, 1)

    # Use IsolationForest with contamination='auto' (threshold at offset=-0.5)
    # Then post-filter: only flag points whose z-score > 2.0
    # This prevents false positives on minor natural income variation
    model = IsolationForest(
        n_estimators=100,
        contamination='auto',
        random_state=42,
        n_jobs=-1
    )

    model.fit(amounts)
    scores = model.score_samples(amounts)

    # Calculate z-scores for gating: only flag if statistically extreme
    mean_val = np.mean(monthly_amounts)
    std_val = np.std(monthly_amounts) if np.std(monthly_amounts) > 0 else 1.0

    anomalous_indices = []
    for i, amount in enumerate(monthly_amounts):
        z = abs(amount - mean_val) / std_val
        # Gate 1: Zero income months are always suspicious if model flags them
        if amount == 0 and scores[i] < -0.45:
            anomalous_indices.append(i)
        # Gate 2: Non-zero amounts need both low isolation score AND high z-score
        elif scores[i] < -0.5 and z > 2.0:
            anomalous_indices.append(i)

    # Model confidence scales with sample size
    # 3 months = low confidence, 6 months = full confidence
    model_confidence = min(1.0, len(monthly_amounts) / 6.0)

    # Build a human-readable reason if anomalies found
    reason = None
    if anomalous_indices:
        normal_indices = [i for i in range(len(monthly_amounts)) if i not in anomalous_indices]
        normal_mean = (
            np.mean([monthly_amounts[i] for i in normal_indices])
            if normal_indices
            else mean_val
        )
        anomalous_values = [monthly_amounts[i] for i in anomalous_indices]

        if any(v > normal_mean * 2 for v in anomalous_values):
            reason = (
                "Income spike detected - one or more months show unusually "
                "high earnings compared to the worker's typical pattern."
            )
        elif any(v == 0 for v in anomalous_values):
            reason = (
                f"Zero-income months detected - the worker had no recorded "
                f"gig income in {len(anomalous_indices)} month(s)."
            )
        else:
            reason = (
                f"Unusual income pattern detected in {len(anomalous_indices)} "
                f"month(s). Manual review recommended."
            )

    return {
        "anomaly_detected": len(anomalous_indices) > 0,
        "anomalous_indices": anomalous_indices,
        "anomaly_scores": scores.tolist(),
        "model_confidence": round(float(model_confidence), 2),
        "reason": reason,
        "skipped": False,
        "skip_reason": None
    }


def get_anomaly_severity(anomaly_result: Dict[str, Any]) -> str:
    """
    Classifies the severity of detected anomalies.
    Returns: 'none' | 'low' | 'medium' | 'high'

    Used to decide whether to hard-block the upload, flag for review,
    or just log silently.
    """
    if not anomaly_result["anomaly_detected"]:
        return "none"

    # Low confidence model (< 3 months of data) = low severity regardless
    if anomaly_result["model_confidence"] < 0.5:
        return "low"

    # Count how many months are anomalous relative to total
    num_anomalous = len(anomaly_result["anomalous_indices"])
    total_months = len(anomaly_result["anomaly_scores"])
    anomaly_ratio = num_anomalous / total_months

    # More than 33% of months are anomalous — high severity
    if anomaly_ratio > 0.33:
        return "high"

    # 1-2 anomalous months — medium severity
    if num_anomalous <= 2:
        return "medium"

    return "high"
