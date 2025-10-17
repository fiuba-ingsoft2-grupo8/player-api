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


@router.post("/tracks", status_code=201)
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

    # DB
    try:
        db_res = supabase.table("tracks").insert({"id": track_id, "audio_path": object_path}).execute()
    except APIError as e:
        if getattr(e, "code", None) in ("23505", 23505):
            raise HTTPException(409, "Track ya existe (id o audio_path duplicado)")
        raise HTTPException(500, f"Error guardando en DB: {getattr(e, 'message', str(e))}")

    if not db_res or not getattr(db_res, "data", None):
        raise HTTPException(500, "Insert en DB no devolvió datos")

    public_url = supabase.storage.from_(BUCKET).get_public_url(object_path)
    return {
        "id": track_id,
        "audio_path": object_path,
        "mime_type": mime_type,
        "public_url": public_url,
    }


@router.get("/tracks/{track_id}")
def get_track_url(track_id: str):
    """Devuelve la URL firmada (válida por 15 minutos) del track."""
    # Buscar el path en la DB
    db_res = supabase.table("tracks").select("audio_path").eq("id", track_id).execute()
    if not db_res.data:
        raise HTTPException(404, "Track no encontrado")

    audio_path = db_res.data[0]["audio_path"]

    public_url = supabase.storage.from_(BUCKET).get_public_url(audio_path)
    return {"url": public_url}