from fastapi import APIRouter, HTTPException
from typing import List
import schemas as s
import repositories as repo
from utils import make_audio_url, make_image_url
from resources.logger import logger

router = APIRouter()

# === Obtener álbum por artista+titulo ===
@router.get("/{artist_name}/albums/{album_title}", response_model=s.AlbumWithTracks)
def get_album_by_artist_and_title(artist_name: str, album_title: str):
    artist = repo.get_artist_by_name(artist_name)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    album = repo.get_album_by_title(artist["id"], album_title)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    tracks_raw = repo.list_tracks_by_album(album["id"])
    tracks: List[s.Track] = []
    for t in tracks_raw:
        tracks.append(s.Track(
            id=t["id"],
            title=t["title"],
            duration_ms=t.get("duration_ms"),
            mime_type=t.get("mime_type"),
            explicit=t.get("explicit", False),
            audio_path=t["audio_path"],
            audio_url=make_audio_url(t["audio_path"]),
        ))

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