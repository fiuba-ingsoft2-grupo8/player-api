from .supabase_client import get_supabase
from .config import settings

sb = get_supabase()

def _normalize_object_path(bucket: str, path: str) -> str | None:
    """Acepta paths con o sin el nombre del bucket y devuelve el path relativo al bucket."""
    if not path:
        return None
    # limpiar espacios laterales y barras duplicadas
    path = path.strip().lstrip("/")
    prefix = f"{bucket}/"
    if path.startswith(prefix):
        path = path[len(prefix):]
    return path

def signed_download_url(bucket: str, path: str, ttl: int | None = None) -> str | None:
    """Genera una URL firmada de descarga para un objeto de Storage."""
    obj_path = _normalize_object_path(bucket, path)
    if not obj_path:
        return None
    ttl = ttl or settings.signed_url_ttl
    res = sb.storage.from_(bucket).create_signed_url(obj_path, ttl)
    return res.get("signedURL") or res.get("signed_url")

def make_audio_url(path: str) -> str | None:
    return signed_download_url(settings.audio_bucket, path, settings.signed_url_ttl)

def make_image_url(path: str) -> str | None:
    return signed_download_url(settings.images_bucket, path, settings.signed_url_ttl)
