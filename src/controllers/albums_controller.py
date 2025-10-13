from fastapi import APIRouter, HTTPException
from typing import List
import schemas as s
import repositories as repo
from utils import make_audio_url, make_image_url
from resources.logger import logger

router = APIRouter()

# === Obtener álbum por ID ===
@router.get("/albums/{album_id}", response_model=s.AlbumWithTracks)
def get_album_by_id(album_id: str):
    album = repo.get_album_by_id(album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    artist = repo.get_artist_by_id(album["artist_id"])
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    tracks_raw = repo.list_tracks_by_album(album["id"])
    tracks: List[s.Track] = [
        s.Track(
            id=t["id"],
            title=t["title"],
            duration_ms=t.get("duration_ms"),
            mime_type=t.get("mime_type"),
            explicit=t.get("explicit", False),
            audio_path=t["audio_path"],
            audio_url=make_audio_url(t["audio_path"]),
        )
        for t in tracks_raw
    ]

    album_out = s.Album(
        id=album["id"],
        title=album["title"],
        cover_path=album.get("cover_path"),
        cover_url=make_image_url(album.get("cover_path")) if album.get("cover_path") else None,
    )

    return s.AlbumWithTracks(
        artist=s.Artist(**artist),
        album=album_out,
        tracks=tracks
    )