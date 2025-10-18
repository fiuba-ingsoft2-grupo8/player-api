from pydantic import BaseModel
from typing import Optional, List

class Track(BaseModel):
    id: str
    duration_ms: Optional[int] = None
    mime_type: Optional[str] = None
    audio_path: str
    audio_url: Optional[str] = None  # signed URL (se setea al vuelo)

class Album(BaseModel):
    id: str
    title: str
    cover_path: Optional[str] = None
    cover_url: Optional[str] = None  # signed URL

class Artist(BaseModel):
    id: str
    name: str

class AlbumWithTracks(BaseModel):
    artist: Artist
    album: Album
    tracks: List[Track]

class Health(BaseModel):
    status: str

class TrackCreate(BaseModel):
    id: str
    duration_ms: Optional[int] = None
    mime_type: Optional[str] = None
    audio_path: str