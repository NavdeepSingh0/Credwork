# Credwork - Income Verification for India's Gig & Domestic Workers

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.1.6-black.svg?logo=next.js)](https://nextjs.org/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E.svg?logo=supabase)](https://supabase.com/)

## 📖 Overview

**Credwork** is a comprehensive income verification platform designed for India's informal workforce — gig workers (delivery riders, drivers, etc.) and domestic workers. The platform analyzes bank statements to extract UPI transaction data, calculates a **GigScore** (income credibility metric), and generates bank-ready PDF income certificates.

The platform also includes **ServiConnect**, a payment rail that enables households to make digital payments to domestic workers, automatically updating their income certificates in real-time.

### Key Features

- **📄 Bank Statement Analysis**: Upload PDF bank statements → automatic UPI transaction extraction using VPA pattern matching
- **🛡️ Fraud Detection**: Multi-layer fraud detection including PDF metadata analysis, font consistency checks, and statistical anomaly detection
- **📊 GigScore Algorithm**: Proprietary income credibility scoring based on transaction frequency, amount consistency, and source diversity
- **📜 Income Certificates**: Auto-generated PDF certificates with QR codes for verification
- **💳 ServiConnect Payment System**: Household-to-worker payment flow with Razorpay UPI integration simulation
- **🌐 Bilingual Support**: Full English and Hindi (हिंदी) localization
- **📱 Mobile-First Design**: Responsive web app optimized for mobile devices

---

## 🏗️ Project Structure

```
/workspace
├── Credwork Backend/          # FastAPI backend server
│   ├── app/
│   │   ├── config/           # Database & settings configuration
│   │   ├── models/           # Pydantic data models
│   │   ├── routes/           # API route handlers
│   │   ├── utils/            # Utility functions (fraud, certs, scores)
│   │   └── ml/               # Machine learning (anomaly detection)
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── vercel.json           # Vercel deployment config
│   └── CREDWORK_BACKEND.md   # Backend engineering documentation
│
├── landing-page/             # Next.js marketing website
│   ├── app/                  # Next.js 16 app directory
│   ├── components/           # React components (sections, UI)
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utility libraries
│   ├── public/               # Static assets
│   └── package.json          # Node.js dependencies
│
├── logo/                     # Brand assets (PNG files)
├── credwork-design-document.md        # Product design specification
├── credwork-framework.md              # Implementation framework
└── workli-gig-detection.md            # Gig worker detection logic
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for landing page)
- **Supabase account** (free tier works)
- **pnpm** or **npm** (for landing page)

### Backend Setup

```bash
cd "Credwork Backend"

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your Supabase credentials
cat > .env << EOF
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
JWT_SECRET=change-this-to-something-random-in-prod
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=30
APP_ENV=development
DEBUG=true
EOF

# Run database migrations (apply supabase_schema.sql in Supabase SQL Editor)

# Start the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

### Landing Page Setup

```bash
cd landing-page

# Install dependencies (pnpm recommended)
pnpm install
# or
npm install

# Start development server
pnpm dev
# or
npm run dev
```

The landing page will be available at `http://localhost:3000`.

---

## 📡 API Endpoints

### Authentication (`/auth`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/request-otp` | Request OTP for phone number |
| POST | `/auth/verify-otp` | Verify OTP and get JWT token |
| POST | `/auth/logout` | Invalidate user session |

### Worker Profile (`/worker`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/worker/profile` | Get current worker profile |
| PUT | `/worker/profile` | Update worker profile |
| GET | `/worker/certificates` | List all certificates |

### Bank Statement Upload (`/upload`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/statement` | Upload bank statement PDF |
| GET | `/upload/status/{upload_id}` | Check processing status |
| GET | `/upload/income-summary` | Get aggregated income data |

### Certificates (`/certificates`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/certificates/latest` | Download latest certificate PDF |
| GET | `/certificates/{id}` | Get specific certificate |
| POST | `/certificates/verify/{qr_code}` | Verify certificate authenticity |

### Household & Domestic Workers (`/household`, `/domestic`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/household/add-worker` | Add domestic worker to household |
| POST | `/household/payment` | Make payment to worker (UPI) |
| GET | `/household/history` | Get payment history |
| GET | `/domestic/workers` | List employing households |
| GET | `/domestic/income` | Get income from all sources |

### Admin (`/admin`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/dashboard` | Admin overview metrics |
| GET | `/admin/users` | List all users (paginated) |
| POST | `/admin/flag/{user_id}` | Flag user for review |

---

## 🔧 Core Components

### 1. Fraud Detection (`app/utils/fraud.py`)
Multi-layer fraud detection system:
- **PDF Metadata Analysis**: Checks creation/modification timestamps, producer software
- **Font Consistency**: Detects mixed fonts indicating text manipulation
- **Statistical Anomalies**: Benford's Law analysis on transaction amounts
- **ML-Based Detection**: Isolation Forest algorithm for outlier detection

### 2. VPA Parser (`app/utils/vpa_parser.py`)
Extracts UPI transactions from bank statements:
- Pattern matching for VPA addresses (e.g., `username@bank`, `mobile@upi`)
- Categorization by counterparty type (merchant, P2P, business)
- Monthly aggregation with conflict resolution

### 3. GigScore Algorithm (`app/utils/gigscore.py`)
Proprietary income credibility score (0-1000):
```
GigScore = f(transaction_frequency, amount_consistency, source_diversity, tenure)
```
Factors considered:
- Number of unique paying counterparties
- Month-over-month income stability
- Transaction frequency patterns
- Absence of fraudulent indicators

### 4. Certificate Generator (`app/utils/cert_generator.py`)
Generates professional PDF certificates using ReportLab:
- Income summary tables (6-month breakdown)
- GigScore visualization
- QR code for instant verification
- Official Credwork branding and signatures

### 5. Conflict Resolver (`app/utils/conflict_resolver.py`)
Handles duplicate or conflicting transaction entries:
- Time-window based deduplication
- Amount-based priority rules
- Source reliability scoring

---

## 🗄️ Database Schema

The application uses Supabase (PostgreSQL) with the following core tables:

- **`users`**: User accounts (workers, households, admins)
- **`worker_profiles`**: Gig/domestic worker details
- **`households`**: Household employer information
- **`uploads`**: Bank statement upload tracking
- **`transactions`**: Extracted UPI transactions
- **`monthly_income`**: Aggregated monthly income records
- **`certificates`**: Generated certificate metadata
- **`payments`**: ServiConnect payment records
- **`otp_requests`**: OTP authentication tracking

See `supabase_schema.sql` for complete DDL statements.

---

## 🧪 Testing

### Run All Tests
```bash
cd "Credwork Backend"
pytest
```

### Test Suites
| File | Coverage |
|------|----------|
| `test_auth.py` | OTP flow, JWT generation |
| `test_pipeline.py` | End-to-end upload → certificate |
| `test_ml.py` | Anomaly detection accuracy |
| `test_phase2.py` | VPA extraction validation |
| `test_phase3.py` | GigScore calculation |
| `test_e2e.py` | Full user journey |
| `test_hh_endpoints.py` | Household payment flow |

---

## 🌐 Deployment

### Backend (Vercel)
```bash
cd "Credwork Backend"
vercel deploy --prod
```

Environment variables must be configured in Vercel dashboard:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`
- `JWT_SECRET`

### Landing Page (Vercel)
```bash
cd landing-page
vercel deploy --prod
```

---

## 🎨 Tech Stack

### Backend
| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.109.2 |
| Database | Supabase (PostgreSQL) |
| PDF Parsing | pdfplumber, pikepdf |
| PDF Generation | reportlab |
| ML/Anomaly Detection | scikit-learn, pandas, numpy |
| Authentication | python-jose (JWT), passlib |
| Validation | pydantic, pydantic-settings |

### Frontend (Landing Page)
| Component | Technology |
|-----------|------------|
| Framework | Next.js 16.1.6 |
| Language | TypeScript 5.7.3 |
| Styling | Tailwind CSS 4.2.0 |
| UI Components | Radix UI primitives |
| Animations | Framer Motion |
| Forms | react-hook-form + zod |
| Charts | Recharts |

---

## 👥 User Roles

### Gig Worker
- Uploads bank statements for income verification
- Receives GigScore and income certificate
- Shares certificate with banks/NBFCs for loans

### Domestic Worker
- Receives digital payments from households via ServiConnect
- Auto-generates income certificate from payment history
- No manual upload required

### Household Employer
- Adds domestic workers to their account
- Makes UPI payments through Razorpay simulation
- Views payment history and tax summaries

### Admin
- Monitors platform usage and fraud flags
- Manages user accounts
- Generates platform analytics

---

## 📝 Documentation

Detailed documentation is available in the following files:

| Document | Description |
|----------|-------------|
| `CREDWORK_BACKEND.md` | Complete backend engineering guide |
| `credwork-design-document.md` | Product design & screen specifications |
| `credwork-framework.md` | Implementation framework |
| `workli-gig-detection.md` | Gig worker classification logic |
| `credwork-ui-fixes.md` | UI improvement tracker |

---

## 🔐 Security Considerations

- **JWT-based authentication** with configurable expiry
- **OTP verification** for all user sign-ins
- **PDF fraud detection** before processing
- **Rate limiting** on sensitive endpoints (recommended for production)
- **Environment variable** management for secrets
- **CORS configuration** for controlled origin access

---

## 🚧 Known Limitations (Hackathon Version)

1. **SMS OTP**: Currently stubbed to console output (use real SMS service in production)
2. **Razorpay Integration**: Simulated mode (enable live mode with API keys)
3. **OCR Fallback**: Tesseract OCR included but not fully tested on scanned PDFs
4. **File Storage**: Local `/tmp` storage (use S3/Supabase Storage in production)

---

## 📄 License

This project is proprietary software developed for hackathon purposes. All rights reserved.

---

## 🙏 Acknowledgments

Built for India's 400M+ informal workers who deserve financial inclusion and credit access.

**Tagline**: *"Your work. Your proof. Your credit."*  
**Hindi**: *"आपका काम. आपका सबूत. आपका क्रेडिट."*

---

## 📞 Contact

For questions or collaboration opportunities, please reach out to the development team.

---

*Last updated: June 2025*
