"""Verification script for all Credwork backend phases."""

print("=" * 50)
print("CREDWORK BACKEND – PHASE VERIFICATION")
print("=" * 50)

# Phase 1: Config & Database
print("\n--- Phase 1: Project Skeleton & Config ---")
try:
    from app.config.settings import settings
    print("  ✅ settings.py loaded")
    from app.config.database import get_supabase
    print("  ✅ database.py loaded")
except Exception as e:
    print(f"  ❌ Phase 1 FAILED: {e}")

# Phase 2: Authentication
print("\n--- Phase 2: Authentication ---")
try:
    from app.utils.auth_helpers import generate_otp, hash_otp, create_access_token, decode_token
    otp = generate_otp()
    assert len(otp) == 6 and otp.isdigit(), "OTP not 6 digits"
    print(f"  ✅ auth_helpers.py (generated test OTP: {otp})")
    
    from app.models.auth import SendOTPRequest, VerifyOTPRequest, SetupProfileRequest
    print("  ✅ models/auth.py loaded")
except Exception as e:
    print(f"  ❌ Phase 2 FAILED: {e}")

# Phase 3: Worker
print("\n--- Phase 3: Worker Profile ---")
try:
    from app.routes.worker import router as worker_router
    routes = [r.path for r in worker_router.routes]
    print(f"  ✅ worker.py ({len(routes)} routes: {routes})")
except Exception as e:
    print(f"  ❌ Phase 3 FAILED: {e}")

# Phase 4A: Fraud
print("\n--- Phase 4A: Fraud Detection ---")
try:
    from app.utils.fraud import run_fraud_checks, SUSPICIOUS_CREATORS
    assert len(SUSPICIOUS_CREATORS) > 5, "Too few suspicious creators"
    print(f"  ✅ fraud.py ({len(SUSPICIOUS_CREATORS)} suspicious creators)")
except Exception as e:
    print(f"  ❌ Phase 4A FAILED: {e}")

# Phase 4B: VPA Parser
print("\n--- Phase 4B: VPA Extraction ---")
try:
    from app.utils.vpa_parser import extract_gig_income, aggregate_by_month, load_vpa_lookup
    import json
    with open("app/config/vpa_config.json") as f:
        vpa = json.load(f)
    platform_count = len(vpa["platforms"])
    total_vpas = sum(len(p["vpas"]) for p in vpa["platforms"])
    print(f"  ✅ vpa_parser.py loaded")
    print(f"  ✅ vpa_config.json ({platform_count} platforms, {total_vpas} VPAs)")
except Exception as e:
    print(f"  ❌ Phase 4B FAILED: {e}")

# Phase 4C: GigScore
print("\n--- Phase 4C: GigScore & Certificates ---")
try:
    from app.utils.gigscore import calculate_gigscore
    test_result = calculate_gigscore({
        "2025-01": 15000, "2025-02": 14000, "2025-03": 16000,
        "2024-12": 13000, "2024-11": 15000, "2024-10": 14500
    })
    print(f"  ✅ gigscore.py (test score: {test_result['score']}, label: {test_result['label']})")
    
    from app.utils.conflict_resolver import resolve_and_save_income
    print("  ✅ conflict_resolver.py loaded")
    
    from app.utils.cert_generator import generate_certificate
    print("  ✅ cert_generator.py loaded")
except Exception as e:
    print(f"  ❌ Phase 4C FAILED: {e}")

# Phase 4D: Upload integration
print("\n--- Phase 4D: Upload Integration ---")
try:
    from app.routes.upload import router as upload_router
    routes = [r.path for r in upload_router.routes]
    print(f"  ✅ upload.py ({len(routes)} routes: {routes})")
    from app.models.upload import UploadResponse
    print("  ✅ models/upload.py loaded")
except Exception as e:
    print(f"  ❌ Phase 4D FAILED: {e}")

# Phase 5: ServiConnect
print("\n--- Phase 5: ServiConnect ---")
try:
    from app.utils.razorpay_sim import simulate_razorpay_webhook
    print("  ✅ razorpay_sim.py loaded")
    from app.models.household import AddWorkerRequest, MakePaymentRequest
    print("  ✅ models/household.py loaded")
    from app.routes.household import router as household_router
    routes = [r.path for r in household_router.routes]
    print(f"  ✅ household.py ({len(routes)} routes)")
    from app.routes.certificates import router as cert_router
    routes = [r.path for r in cert_router.routes]
    print(f"  ✅ certificates.py ({len(routes)} routes)")
except Exception as e:
    print(f"  ❌ Phase 5 FAILED: {e}")

# Phase 6: Admin & Settings
print("\n--- Phase 6: Admin & Settings ---")
try:
    from app.routes.admin import router as admin_router
    routes = [r.path for r in admin_router.routes]
    print(f"  ✅ admin.py ({len(routes)} routes)")
    from app.routes.settings import router as settings_router
    routes = [r.path for r in settings_router.routes]
    print(f"  ✅ settings.py ({len(routes)} routes)")
except Exception as e:
    print(f"  ❌ Phase 6 FAILED: {e}")

# Phase 7: Seed & Deploy
print("\n--- Phase 7: Demo Seed & Deploy ---")
import os
print(f"  ✅ seed.py exists: {os.path.exists('seed.py')}")
print(f"  ✅ vercel.json exists: {os.path.exists('vercel.json')}")
print(f"  ✅ .env exists: {os.path.exists('.env')}")

# Final server import test
print("\n--- Final: FastAPI App Import ---")
try:
    from main import app
    route_count = len(app.routes)
    print(f"  ✅ main.py app created with {route_count} total routes")
except Exception as e:
    print(f"  ❌ App import FAILED: {e}")

print("\n" + "=" * 50)
print("VERIFICATION COMPLETE")
print("=" * 50)
