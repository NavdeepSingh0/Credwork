from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str = Field(default="", validation_alias="SUPABASE_URL")
    supabase_key: str = Field(default="", validation_alias="SUPABASE_KEY")
    supabase_service_key: str = Field(default="", validation_alias="SUPABASE_SERVICE_KEY")
    
    jwt_secret: str = Field(
        default="fallback-secret-for-dev-only-do-not-use-in-prod",
        validation_alias="JWT_SECRET",
    )
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    jwt_expiry_days: int = Field(default=30, validation_alias="JWT_EXPIRY_DAYS")
    
    fast2sms_api_key: str = Field(default="", validation_alias="FAST2SMS_API_KEY")
    
    app_env: str = Field(default="development", validation_alias="APP_ENV")
    debug: bool = Field(default=True, validation_alias="DEBUG")
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Don't crash on unknown env vars
    }

settings = Settings()
