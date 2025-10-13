from supabase import create_client, Client
from config import settings
from resources.logger import logger

def get_supabase() -> Client:
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY")
    return create_client(settings.supabase_url, settings.supabase_service_role_key)
