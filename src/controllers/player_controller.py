import os
import mimetypes
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from supabase import create_client, Client
from fastapi import HTTPException
from postgrest.exceptions import APIError

router = APIRouter()

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@router.post("/tracks/upload", status_code=201)
async def upload_track(
    track_id: str = Form(...),
    audio: UploadFile = File(...),
    upsert: bool = Form(False),
):
    if not track_id.strip():
        raise HTTPException(400, "track_id requerido")

    mime_type = (
        audio.content_type
        or mimetypes.guess_type(audio.filename or "")[0]
        or "application/octet-stream"
    )

    ext = ""
    if audio.filename and "." in audio.filename:
        ext = "." + audio.filename.rsplit(".", 1)[-1].lower()

    if ext == ".mp3":
        bucket = "tracks"
    elif ext in [".mp4", ".mov", ".avi"]:
        bucket = "videos"
    else:
        raise HTTPException(400, "Tipo de archivo no soportado")

    object_path = f"{track_id}{ext}"

    content = await audio.read()
    if not content:
        raise HTTPException(400, "archivo vacío")

    try:
        if upsert:
            supabase.storage.from_(bucket).update(
                object_path, content, {"contentType": mime_type}
            )
        else:
            supabase.storage.from_(bucket).upload(
                object_path, content, {"contentType": mime_type}
            )
    except Exception as e:
        raise HTTPException(500, f"Error subiendo archivo: {e}")

    public_url = supabase.storage.from_(bucket).get_public_url(object_path)

    return {
        "id": track_id,
        "path": object_path,
        "mime_type": mime_type,
        "bucket": bucket,
        "public_url": public_url,
    }


@router.get("/tracks/{track_id}")
def get_track_url(track_id: str):
    # 1) Buscar en bucket tracks (.mp3)
    audio_ext = ".mp3"
    audio_path = f"{track_id}{audio_ext}"

    # Intentamos ver si existe el archivo .mp3
    try:
        files = supabase.storage.from_("tracks").list("", {"search": track_id})
        if any(f["name"] == audio_path for f in files):
            url = supabase.storage.from_("tracks").get_public_url(audio_path)
            return {
                "bucket": "tracks",
                "path": audio_path,
                "url": url,
            }
    except Exception:
        pass

    # 2) Si no está en tracks, buscamos en videos con extensiones múltiples
    video_exts = [".mp4", ".mov", ".avi"]
    files = supabase.storage.from_("videos").list("", {"search": track_id})

    for f in files:
        for ext in video_exts:
            if f["name"] == f"{track_id}{ext}":
                url = supabase.storage.from_("videos").get_public_url(f["name"])
                return {
                    "bucket": "videos",
                    "path": f["name"],
                    "url": url,
                }

    # 3) Si no existe en ningún lado → 404
    raise HTTPException(404, f"No se encontró ningún archivo para track_id '{track_id}'")