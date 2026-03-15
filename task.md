# Backend Rebuild Task List

## Phase 1: Core & Authentication
- [x] Define precise Pydantic models matching frontend [User](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/credwork/src/store/AuthContext.tsx#4-13) interface ([app/models/auth.py](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/app/models/auth.py)).
- [x] Re-implement `POST /auth/send-otp` (include backdoor `123456`).
- [x] Re-implement `POST /auth/verify-otp` (handle `existing_user` and `new_user`).
- [x] Re-implement `POST /auth/setup-profile` (validate and insert).
- [x] Re-implement `GET /auth/me`.

## Phase 2: Verification Fixes & Gig Worker Flow
- [x] Fix amount extraction bug in [app/utils/vpa_parser.py](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/app/utils/vpa_parser.py) (avoid taking balance column).
- [x] Relax fraud detection checks in [app/utils/fraud.py](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/app/utils/fraud.py).
- [x] Re-implement `GET /worker/dashboard` (match `DEMO_GIG_WORKER`).
- [x] Re-implement `GET /worker/income`.
- [x] Re-implement `POST /upload/statement` (synchronous full pipeline, return correct schema).
- [x] Re-implement `GET /upload/status/{upload_id}`.
- [x] Implement `GET /certificates` and `GET /certificates/{cert_id}` in [app/routes/certificates.py](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/app/routes/certificates.py).

## Phase 3: Household & Domestic Worker
- [x] Define Pydantic models for household requests (`add-worker`, [payment](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/app/routes/household.py#219-263)).
- [x] Re-implement `GET /household/dashboard` (match `DEMO_HOUSEHOLD`).
- [x] Re-implement `POST /household/add-worker` and `POST /household/payment`.
- [x] Re-implement payment polling and history routes.
- [x] Create [app/routes/domestic.py](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/app/routes/domestic.py) and implement `GET /domestic/dashboard` (match `DEMO_DOMESTIC_WORKER`).

## Phase 4: Integration
- [x] Register all new routers in [main.py](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/main.py). (already done)
- [x] Update [seed.py](file:///c:/Users/ns708/OneDrive/Desktop/hack%20energy/Credwork%20Backend/seed.py) to correctly populate the database matching the new business logic. (added payment_date)
- [x] Test End-to-End: Gig worker auth -> upload -> success.
- [x] Test End-to-End: Household auth -> view dashboard.
- [x] Test End-to-End: Domestic worker auth -> view dashboard.
