# Imports.
import pytest
import os
import sys

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from schemas import Track, Album, Artist, AlbumWithTracks, Health, TrackCreate

# Test class for Track schema.
class TestTrackSchema:
    def test_track_with_all_fields(self):
        """Test creating Track with all fields."""
        track = Track(
            id="track_123",
            duration_ms=180000,
            mime_type="audio/mpeg",
            audio_path="/audio/track.mp3",
            audio_url="https://example.com/track.mp3"
        )
        
        assert track.id == "track_123"
        assert track.duration_ms == 180000
        assert track.mime_type == "audio/mpeg"
        assert track.audio_path == "/audio/track.mp3"
        assert track.audio_url == "https://example.com/track.mp3"
    
    def test_track_with_required_fields_only(self):
        """Test creating Track with only required fields."""
        track = Track(
            id="track_456",
            audio_path="/audio/track.mp3"
        )
        
        assert track.id == "track_456"
        assert track.audio_path == "/audio/track.mp3"
        assert track.duration_ms is None
        assert track.mime_type is None
        assert track.audio_url is None
    
    def test_track_optional_fields_none(self):
        """Test that optional fields default to None."""
        track = Track(
            id="track_789",
            audio_path="/audio/track.mp3",
            duration_ms=None,
            mime_type=None
        )
        
        assert track.duration_ms is None
        assert track.mime_type is None

# Test class for Album schema.
class TestAlbumSchema:
    def test_album_with_all_fields(self):
        """Test creating Album with all fields."""
        album = Album(
            id="album_123",
            title="Abbey Road",
            cover_path="/covers/abbey.jpg",
            cover_url="https://example.com/covers/abbey.jpg"
        )
        
        assert album.id == "album_123"
        assert album.title == "Abbey Road"
        assert album.cover_path == "/covers/abbey.jpg"
        assert album.cover_url == "https://example.com/covers/abbey.jpg"
    
    def test_album_with_required_fields_only(self):
        """Test creating Album with only required fields."""
        album = Album(
            id="album_456",
            title="Dark Side of the Moon"
        )
        
        assert album.id == "album_456"
        assert album.title == "Dark Side of the Moon"
        assert album.cover_path is None
        assert album.cover_url is None

# Test class for Artist schema.
class TestArtistSchema:
    def test_artist_creation(self):
        """Test creating Artist with all fields."""
        artist = Artist(
            id="artist_123",
            name="The Beatles"
        )
        
        assert artist.id == "artist_123"
        assert artist.name == "The Beatles"
    
    def test_artist_with_different_name(self):
        """Test creating Artist with different name."""
        artist = Artist(
            id="artist_456",
            name="Pink Floyd"
        )
        
        assert artist.id == "artist_456"
        assert artist.name == "Pink Floyd"

# Test class for AlbumWithTracks schema.
class TestAlbumWithTracksSchema:
    def test_album_with_tracks_full(self):
        """Test creating AlbumWithTracks with full data."""
        artist = Artist(id="artist_1", name="The Beatles")
        album = Album(id="album_1", title="Abbey Road", cover_path="/covers/abbey.jpg")
        tracks = [
            Track(id="track_1", audio_path="/audio/track1.mp3", duration_ms=180000),
            Track(id="track_2", audio_path="/audio/track2.mp3", duration_ms=200000)
        ]
        
        album_with_tracks = AlbumWithTracks(
            artist=artist,
            album=album,
            tracks=tracks
        )
        
        assert album_with_tracks.artist.id == "artist_1"
        assert album_with_tracks.artist.name == "The Beatles"
        assert album_with_tracks.album.id == "album_1"
        assert album_with_tracks.album.title == "Abbey Road"
        assert len(album_with_tracks.tracks) == 2
        assert album_with_tracks.tracks[0].id == "track_1"
        assert album_with_tracks.tracks[1].id == "track_2"
    
    def test_album_with_tracks_empty_tracks(self):
        """Test creating AlbumWithTracks with empty tracks list."""
        artist = Artist(id="artist_2", name="Pink Floyd")
        album = Album(id="album_2", title="The Wall")
        
        album_with_tracks = AlbumWithTracks(
            artist=artist,
            album=album,
            tracks=[]
        )
        
        assert album_with_tracks.artist.id == "artist_2"
        assert album_with_tracks.album.id == "album_2"
        assert album_with_tracks.tracks == []

# Test class for Health schema.
class TestHealthSchema:
    def test_health_creation(self):
        """Test creating Health schema."""
        health = Health(status="ok")
        
        assert health.status == "ok"
    
    def test_health_different_status(self):
        """Test creating Health with different status."""
        health = Health(status="degraded")
        
        assert health.status == "degraded"

# Test class for TrackCreate schema.
class TestTrackCreateSchema:
    def test_track_create_with_all_fields(self):
        """Test creating TrackCreate with all fields."""
        track_create = TrackCreate(
            id="track_new",
            duration_ms=250000,
            mime_type="audio/mpeg",
            audio_path="/audio/new_track.mp3"
        )
        
        assert track_create.id == "track_new"
        assert track_create.duration_ms == 250000
        assert track_create.mime_type == "audio/mpeg"
        assert track_create.audio_path == "/audio/new_track.mp3"
    
    def test_track_create_with_required_fields_only(self):
        """Test creating TrackCreate with only required fields."""
        track_create = TrackCreate(
            id="track_new2",
            audio_path="/audio/new_track2.mp3"
        )
        
        assert track_create.id == "track_new2"
        assert track_create.audio_path == "/audio/new_track2.mp3"
        assert track_create.duration_ms is None
        assert track_create.mime_type is None
    
    def test_track_create_optional_fields_none(self):
        """Test that optional fields in TrackCreate default to None."""
        track_create = TrackCreate(
            id="track_new3",
            audio_path="/audio/new_track3.mp3",
            duration_ms=None,
            mime_type=None
        )
        
        assert track_create.duration_ms is None
        assert track_create.mime_type is None

