from typing import Any
from supabase import create_client, Client
from pydantic import BaseModel

from app.config.settings import settings

class SupabaseSingleton:
    _instance: Client | None = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            # Setup the service role key for bypassing RLS during hackathon demo
            cls._instance = create_client(
                settings.supabase_url, 
                settings.supabase_service_key
            )
        return cls._instance

def get_supabase() -> Client:
    """Dependency injection helper for FastAPI routes."""
    return SupabaseSingleton.get_client()
