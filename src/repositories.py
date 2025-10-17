from typing import Dict, Any, List, Optional
from supabase_client import get_supabase

sb = get_supabase()

def get_artist_by_name(name: str) -> Optional[Dict[str, Any]]:
    r = sb.table("artists").select("id,name").eq("name", name).limit(1).execute()
    return r.data[0] if r.data else None

def get_album_by_title(artist_id: str, title: str) -> Optional[Dict[str, Any]]:
    r = sb.table("albums").select("id,title,cover_path").eq("artist_id", artist_id).eq("title", title).limit(1).execute()
    return r.data[0] if r.data else None

def get_album_by_id(album_id: str) -> Optional[Dict[str, Any]]:
    r = sb.table("albums").select("id,title,cover_path,artist_id").eq("id", album_id).limit(1).execute()
    return r.data[0] if r.data else None

def get_artist_by_id(artist_id: str) -> Optional[Dict[str, Any]]:
    r = sb.table("artists").select("id,name").eq("id", artist_id).limit(1).execute()
    return r.data[0] if r.data else None

def list_tracks_by_album(album_id: str) -> List[Dict[str, Any]]:
    # Podés cambiar el orden (por created_at, title, position en playlist, etc.)
    r = sb.table("tracks") \
        .select("id,title,duration_ms,mime_type,explicit,audio_path") \
        .eq("album_id", album_id) \
        .order("title", desc=False) \
        .execute()
    return r.data or []

def get_track_by_id(track_id: str) -> Optional[Dict[str, Any]]:
    r = sb.table("tracks").select("id,title,audio_path,mime_type,album_id").eq("id", track_id).limit(1).execute()
    return r.data[0] if r.data else None

    
def create_track(track: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    r = sb.table("tracks").insert(track).execute()
    return r.data[0] if r.data else None