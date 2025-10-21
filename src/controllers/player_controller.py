import os
import mimetypes
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from supabase import create_client, Client
from fastapi import HTTPException
from postgrest.exceptions import APIError

router = APIRouter()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
BUCKET = os.getenv("PLAYER_BUCKET", "tracks")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@router.post("/tracks/upload", status_code=201)
async def upload_track(
    track_id: str = Form(...),
    audio: UploadFile = File(...),
    upsert: bool = Form(False),
):
    if not track_id.strip():
        raise HTTPException(400, "track_id requerido")

    mime_type = audio.content_type or mimetypes.guess_type(audio.filename or "")[0] or "application/octet-stream"
    ext = ""
    if audio.filename and "." in audio.filename:
        ext = "." + audio.filename.rsplit(".", 1)[-1].lower()
    
    if ext != ".mp3":
        raise HTTPException(400, "El archivo debe ser un MP3")

    object_path = f"{track_id}{ext}"

    content = await audio.read()
    if not content:
        raise HTTPException(400, "archivo vacío")

    # Storage
    try:
        if upsert:
            supabase.storage.from_(BUCKET).update(object_path, content, {"contentType": mime_type})
        else:
            supabase.storage.from_(BUCKET).upload(object_path, content, {"contentType": mime_type})
    except Exception as e:
        raise HTTPException(500, f"Error subiendo archivo: {e}")

    public_url = supabase.storage.from_(BUCKET).get_public_url(object_path)
    return {
        "id": track_id,
        "audio_path": object_path,
        "mime_type": mime_type,
        "public_url": public_url,
    }


@router.get("/tracks/{track_id}")
def get_track_url(track_id: str):
    public_url = supabase.storage.from_(BUCKET).get_public_url(track_id + ".mp3")
    return {"url": public_url}