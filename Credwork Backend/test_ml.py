"""Phase 7B ML Demo Tests -- run with: python test_ml.py"""
import sys
sys.path.insert(0, '.')

from app.ml.anomaly_detector import detect_income_anomalies, get_anomaly_severity

# Test 1: Consistent income -- should return no anomaly
consistent = [18000, 19500, 17800, 20000, 18500, 19100]
result1 = detect_income_anomalies(consistent)
assert result1["anomaly_detected"] == False, f"Test 1 FAILED: {result1}"
print(f"PASS Test 1: Consistent income -- no anomaly (confidence: {result1['model_confidence']})")

# Test 2: One massive spike -- should detect anomaly
spike = [18000, 19000, 17500, 18800, 75000, 19200]
result2 = detect_income_anomalies(spike)
assert result2["anomaly_detected"] == True, f"Test 2 FAILED: {result2}"
assert 4 in result2["anomalous_indices"], f"Test 2 FAILED: index 4 not in {result2['anomalous_indices']}"
print(f"PASS Test 2: Spike detected at {result2['anomalous_indices']} -- {result2['reason']}")

# Test 3: Zero-income months -- should detect anomaly
with_zeros = [18000, 0, 19000, 18500, 0, 17800]
result3 = detect_income_anomalies(with_zeros)
assert result3["anomaly_detected"] == True, f"Test 3 FAILED: {result3}"
print(f"PASS Test 3: Zero-income at {result3['anomalous_indices']} -- {result3['reason']}")

# Test 4: Insufficient data -- should skip
too_short = [18000, 19000]
result4 = detect_income_anomalies(too_short)
assert result4["skipped"] == True, f"Test 4 FAILED: {result4}"
print(f"PASS Test 4: Skipped -- {result4['skip_reason']}")

# Severity
sev2 = get_anomaly_severity(result2)
sev3 = get_anomaly_severity(result3)
print(f"\nSeverity spike: {sev2}")
print(f"Severity zeros: {sev3}")

print("\nAll ML model tests passed!")
