from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, upload, worker, certificates, household, settings, admin, domestic

app = FastAPI(
    title="Credwork API",
    description="Income verification for India's gig and domestic workers",
    version="1.0.0",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev (mobile app sends non-standard origins)
    allow_credentials=False,  # Must be False when allow_origins=["*"] (browsers block it otherwise)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Certificates are served from Supabase Storage.
# Avoid creating local directories at import time because Vercel only allows
# runtime writes under /tmp and a write here can crash cold starts.

# Register all routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(worker.router)
app.include_router(certificates.router)
app.include_router(household.router)
app.include_router(domestic.router)
app.include_router(settings.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "name": "Credwork API",
        "version": "1.0.0",
        "status": "live",
        "docs": "/docs"
    }
