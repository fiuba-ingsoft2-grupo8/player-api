# Imports.
from supabase_client import get_supabase
from config import settings

# Inicializar el cliente de Supabase.
sb = get_supabase()

# Functions for generating signed URLs for Supabase Storage objects.
def _normalize_object_path(bucket: str, path: str) -> str | None:
    """It accepts paths with or without the bucket name and returns the path relative to the bucket."""
    if not path:
        return None

    path = path.strip().lstrip("/")
    prefix = f"{bucket}/"
    if path.startswith(prefix):
        path = path[len(prefix):]
    return path

# Functions to generate signed URLs.
def signed_download_url(bucket: str, path: str, ttl: int | None = None) -> str | None:
    """Generates a signed download URL for a Storage object."""
    obj_path = _normalize_object_path(bucket, path)
    if not obj_path:
        return None

    ttl = ttl or settings.signed_url_ttl
    res = sb.storage.from_(bucket).create_signed_url(obj_path, ttl)
    return res.get("signedURL") or res.get("signed_url")

# Specific functions for audio and image URLs.
def make_audio_url(path: str) -> str | None:
    return signed_download_url(settings.audio_bucket, path, settings.signed_url_ttl)

# Specific functions for audio and image URLs.
def make_image_url(path: str) -> str | None:
    return signed_download_url(settings.images_bucket, path, settings.signed_url_ttl)
