from fastapi import APIRouter, HTTPException
from typing import List
import schemas as s
import repositories as repo
from utils import make_audio_url
from resources.logger import logger

router = APIRouter()

# === Obtener URL firmada de un track puntual ===
@router.get("/tracks/{track_id}/url", response_model=s.Track)
def get_track_signed_url(track_id: str):
    t = repo.get_track_by_id(track_id)
    if not t:
        raise HTTPException(status_code=404, detail="Track not found")
    return s.Track(
        id=t["id"],
        title=t["title"],
        duration_ms=t.get("duration_ms"),
        mime_type=t.get("mime_type"),
        explicit=t.get("explicit", False),
        audio_path=t["audio_path"],
        audio_url=make_audio_url(t["audio_path"]),
    )
