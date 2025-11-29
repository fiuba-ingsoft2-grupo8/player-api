# Imports.
from pydantic import BaseModel
import os

# Configuration settings using Pydantic BaseModel.
class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "development")
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    audio_bucket: str = os.getenv("AUDIO_BUCKET", "audio")
    images_bucket: str = os.getenv("IMAGES_BUCKET", "images")
    signed_url_ttl: int = int(os.getenv("SIGNED_URL_TTL", "3600"))

# Instantiate settings.
settings = Settings()
