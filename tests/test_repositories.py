# Imports.
import pytest
import os
import sys
from unittest.mock import MagicMock, Mock

# Set environment variables before importing any application modules.
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key"

# Mock the supabase module before any imports.
sys.modules['supabase'] = MagicMock()

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import repositories as repo

# Test class for artist functions.
class TestArtistFunctions:
    def test_get_artist_by_name_found(self, mock_sb):
        """Test getting an artist by name when it exists."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [{"id": "artist_1", "name": "The Beatles"}]
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_artist_by_name("The Beatles")
        
        assert result is not None
        assert result["id"] == "artist_1"
        assert result["name"] == "The Beatles"
    
    def test_get_artist_by_name_not_found(self, mock_sb):
        """Test getting an artist by name when it doesn't exist."""
        # Setup mock response with empty data
        mock_response = Mock()
        mock_response.data = []
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_artist_by_name("Unknown Artist")
        
        assert result is None
    
    def test_get_artist_by_id_found(self, mock_sb):
        """Test getting an artist by ID when it exists."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [{"id": "artist_2", "name": "Pink Floyd"}]
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_artist_by_id("artist_2")
        
        assert result is not None
        assert result["id"] == "artist_2"
        assert result["name"] == "Pink Floyd"
    
    def test_get_artist_by_id_not_found(self, mock_sb):
        """Test getting an artist by ID when it doesn't exist."""
        # Setup mock response with empty data
        mock_response = Mock()
        mock_response.data = []
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_artist_by_id("nonexistent_id")
        
        assert result is None

# Test class for album functions.
class TestAlbumFunctions:
    def test_get_album_by_title_found(self, mock_sb):
        """Test getting an album by title and artist_id when it exists."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [{
            "id": "album_1",
            "title": "Abbey Road",
            "cover_path": "/covers/abbey.jpg"
        }]
        
        mock_sb.table.return_value.select.return_value.eq.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_album_by_title("artist_1", "Abbey Road")
        
        assert result is not None
        assert result["id"] == "album_1"
        assert result["title"] == "Abbey Road"
        assert result["cover_path"] == "/covers/abbey.jpg"
    
    def test_get_album_by_title_not_found(self, mock_sb):
        """Test getting an album by title when it doesn't exist."""
        # Setup mock response with empty data
        mock_response = Mock()
        mock_response.data = []
        
        mock_sb.table.return_value.select.return_value.eq.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_album_by_title("artist_1", "Unknown Album")
        
        assert result is None
    
    def test_get_album_by_id_found(self, mock_sb):
        """Test getting an album by ID when it exists."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [{
            "id": "album_2",
            "title": "Dark Side of the Moon",
            "cover_path": "/covers/darkside.jpg",
            "artist_id": "artist_2"
        }]
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_album_by_id("album_2")
        
        assert result is not None
        assert result["id"] == "album_2"
        assert result["title"] == "Dark Side of the Moon"
        assert result["artist_id"] == "artist_2"
    
    def test_get_album_by_id_not_found(self, mock_sb):
        """Test getting an album by ID when it doesn't exist."""
        # Setup mock response with empty data
        mock_response = Mock()
        mock_response.data = []
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_album_by_id("nonexistent_id")
        
        assert result is None

# Test class for track functions.
class TestTrackFunctions:
    def test_get_track_by_id_found(self, mock_sb):
        """Test getting a track by ID when it exists."""
        # Setup mock response
        mock_response = Mock()
        mock_response.data = [{
            "id": "track_1",
            "title": "Come Together",
            "audio_path": "/audio/come_together.mp3",
            "mime_type": "audio/mpeg",
            "album_id": "album_1"
        }]
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_track_by_id("track_1")
        
        assert result is not None
        assert result["id"] == "track_1"
        assert result["title"] == "Come Together"
        assert result["audio_path"] == "/audio/come_together.mp3"
    
    def test_get_track_by_id_not_found(self, mock_sb):
        """Test getting a track by ID when it doesn't exist."""
        # Setup mock response with empty data
        mock_response = Mock()
        mock_response.data = []
        
        mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_response
        
        result = repo.get_track_by_id("nonexistent_id")
        
        assert result is None
    
    def test_list_tracks_by_album_with_tracks(self, mock_sb):
        """Test listing tracks for an album that has tracks."""
        # Setup mock response with multiple tracks
        mock_response = Mock()
        mock_response.data = [
            {
                "id": "track_1",
                "title": "Come Together",
                "duration_ms": 259000,
                "mime_type": "audio/mpeg",
                "explicit": False,
                "audio_path": "/audio/come_together.mp3"
            },
            {
                "id": "track_2",
                "title": "Something",
                "duration_ms": 182000,
                "mime_type": "audio/mpeg",
                "explicit": False,
                "audio_path": "/audio/something.mp3"
            }
        ]
        
        mock_sb.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response
        
        result = repo.list_tracks_by_album("album_1")
        
        assert result is not None
        assert len(result) == 2
        assert result[0]["id"] == "track_1"
        assert result[1]["id"] == "track_2"
    
    def test_list_tracks_by_album_empty(self, mock_sb):
        """Test listing tracks for an album with no tracks."""
        # Setup mock response with empty data
        mock_response = Mock()
        mock_response.data = []
        
        mock_sb.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response
        
        result = repo.list_tracks_by_album("album_empty")
        
        assert result == []
    
    def test_list_tracks_by_album_none_response(self, mock_sb):
        """Test listing tracks when response data is None."""
        # Setup mock response with None data
        mock_response = Mock()
        mock_response.data = None
        
        mock_sb.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response
        
        result = repo.list_tracks_by_album("album_1")
        
        assert result == []
    
    def test_create_track_success(self, mock_sb):
        """Test creating a track successfully."""
        # Setup mock response
        track_data = {
            "id": "new_track",
            "title": "New Song",
            "duration_ms": 200000,
            "mime_type": "audio/mpeg",
            "audio_path": "/audio/new_song.mp3",
            "album_id": "album_1"
        }
        
        mock_response = Mock()
        mock_response.data = [track_data]
        
        mock_sb.table.return_value.insert.return_value.execute.return_value = mock_response
        
        result = repo.create_track(track_data)
        
        assert result is not None
        assert result["id"] == "new_track"
        assert result["title"] == "New Song"
    
    def test_create_track_empty_response(self, mock_sb):
        """Test creating a track with empty response."""
        # Setup mock response with empty data
        track_data = {
            "id": "new_track",
            "title": "New Song"
        }
        
        mock_response = Mock()
        mock_response.data = []
        
        mock_sb.table.return_value.insert.return_value.execute.return_value = mock_response
        
        result = repo.create_track(track_data)
        
        assert result is None
    
    def test_create_track_none_response(self, mock_sb):
        """Test creating a track with None response."""
        # Setup mock response with None data
        track_data = {
            "id": "new_track",
            "title": "New Song"
        }
        
        mock_response = Mock()
        mock_response.data = None
        
        mock_sb.table.return_value.insert.return_value.execute.return_value = mock_response
        
        result = repo.create_track(track_data)
        
        assert result is None

