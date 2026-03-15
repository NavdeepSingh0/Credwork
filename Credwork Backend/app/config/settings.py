from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiry_days: int = 30
    
    fast2sms_api_key: str = ""
    
    app_env: str = "development"
    debug: bool = True
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Don't crash on unknown env vars
    }

settings = Settings()
