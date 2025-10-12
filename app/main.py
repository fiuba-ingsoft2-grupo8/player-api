from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .config import settings
from . import repositories as repo
from . import schemas as s
from .utils import make_audio_url, make_image_url

app = FastAPI(title="Melodía API", version="1.0.0")

# CORS
allowed = [o.strip() for o in settings.allowed_origins.split(",")] if settings.allowed_origins else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed if allowed != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=s.Health)
def health():
    return {"status": "ok"}

# === Obtener álbum por artista+titulo ===
@app.get("/artists/{artist_name}/albums/{album_title}", response_model=s.AlbumWithTracks)
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

# === Obtener álbum por ID ===
@app.get("/albums/{album_id}", response_model=s.AlbumWithTracks)
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

# === Obtener URL firmada de un track puntual ===
@app.get("/tracks/{track_id}/url", response_model=s.Track)
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
