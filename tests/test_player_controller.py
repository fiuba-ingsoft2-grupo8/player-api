# Imports.
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch
from io import BytesIO

# Set environment variables before importing any application modules.
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key"

# Mock the supabase module before any imports.
sys.modules['supabase'] = MagicMock()

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from main import app

# Create test client.
client = TestClient(app)

# Test class for upload_track endpoint.
class TestUploadTrack:
    def test_upload_track_missing_track_id(self):
        """Test uploading a track without track_id."""
        # Create a mock file
        file_content = b"fake audio content"
        files = {"audio": ("test.mp3", BytesIO(file_content), "audio/mpeg")}
        data = {"track_id": ""}  # Empty track_id
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 400
        assert "track_id requerido" in response.json()["detail"]
    
    def test_upload_track_whitespace_track_id(self):
        """Test uploading a track with whitespace-only track_id."""
        # Create a mock file
        file_content = b"fake audio content"
        files = {"audio": ("test.mp3", BytesIO(file_content), "audio/mpeg")}
        data = {"track_id": "   "}  # Whitespace only
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 400
        assert "track_id requerido" in response.json()["detail"]
    
    def test_upload_track_unsupported_file_type(self):
        """Test uploading a track with unsupported file type."""
        # Create a mock file with unsupported extension
        file_content = b"fake content"
        files = {"audio": ("test.txt", BytesIO(file_content), "text/plain")}
        data = {"track_id": "track_123"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 400
        assert "Tipo de archivo no soportado" in response.json()["detail"]
    
    def test_upload_track_empty_file(self):
        """Test uploading an empty file."""
        # Create an empty file
        files = {"audio": ("test.mp3", BytesIO(b""), "audio/mpeg")}
        data = {"track_id": "track_123"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 400
        assert "archivo vacío" in response.json()["detail"].lower()
    
    @patch('controllers.player_controller.supabase')
    def test_upload_track_mp3_success(self, mock_supabase):
        """Test successfully uploading an MP3 file."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.upload.return_value = None
        mock_storage.get_public_url.return_value = "https://example.com/tracks/track_123.mp3"
        
        # Create a mock MP3 file
        file_content = b"fake mp3 content"
        files = {"audio": ("test.mp3", BytesIO(file_content), "audio/mpeg")}
        data = {"track_id": "track_123", "upsert": "false"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["id"] == "track_123"
        assert result["bucket"] == "tracks"
        assert result["path"] == "track_123.mp3"
        assert result["mime_type"] == "audio/mpeg"
        assert "public_url" in result
    
    @patch('controllers.player_controller.supabase')
    def test_upload_track_mp4_success(self, mock_supabase):
        """Test successfully uploading an MP4 video file."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.upload.return_value = None
        mock_storage.get_public_url.return_value = "https://example.com/videos/track_456.mp4"
        
        # Create a mock MP4 file
        file_content = b"fake mp4 content"
        files = {"audio": ("test.mp4", BytesIO(file_content), "video/mp4")}
        data = {"track_id": "track_456", "upsert": "false"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["id"] == "track_456"
        assert result["bucket"] == "videos"
        assert result["path"] == "track_456.mp4"
    
    @patch('controllers.player_controller.supabase')
    def test_upload_track_mov_success(self, mock_supabase):
        """Test successfully uploading a MOV video file."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.upload.return_value = None
        mock_storage.get_public_url.return_value = "https://example.com/videos/track_789.mov"
        
        # Create a mock MOV file
        file_content = b"fake mov content"
        files = {"audio": ("test.mov", BytesIO(file_content), "video/quicktime")}
        data = {"track_id": "track_789", "upsert": "false"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["bucket"] == "videos"
        assert result["path"] == "track_789.mov"
    
    @patch('controllers.player_controller.supabase')
    def test_upload_track_avi_success(self, mock_supabase):
        """Test successfully uploading an AVI video file."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.upload.return_value = None
        mock_storage.get_public_url.return_value = "https://example.com/videos/track_101.avi"
        
        # Create a mock AVI file
        file_content = b"fake avi content"
        files = {"audio": ("test.avi", BytesIO(file_content), "video/x-msvideo")}
        data = {"track_id": "track_101"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["bucket"] == "videos"
    
    @patch('controllers.player_controller.supabase')
    def test_upload_track_upsert_mode(self, mock_supabase):
        """Test uploading a track in upsert mode."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.update.return_value = None
        mock_storage.get_public_url.return_value = "https://example.com/tracks/track_upsert.mp3"
        
        # Create a mock MP3 file
        file_content = b"updated content"
        files = {"audio": ("test.mp3", BytesIO(file_content), "audio/mpeg")}
        data = {"track_id": "track_upsert", "upsert": "true"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 201
        # Verify update was called instead of upload
        mock_storage.update.assert_called_once()
    
    @patch('controllers.player_controller.supabase')
    def test_upload_track_storage_error(self, mock_supabase):
        """Test handling storage error during upload."""
        # Setup mock to raise an exception
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.upload.side_effect = Exception("Storage error")
        
        # Create a mock MP3 file
        file_content = b"fake content"
        files = {"audio": ("test.mp3", BytesIO(file_content), "audio/mpeg")}
        data = {"track_id": "track_error"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 500
        assert "Error subiendo archivo" in response.json()["detail"]
    
    @patch('controllers.player_controller.supabase')
    def test_upload_track_no_extension(self, mock_supabase):
        """Test uploading a file without extension."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        
        # Create a mock file without extension
        file_content = b"fake content"
        files = {"audio": ("testfile", BytesIO(file_content), "audio/mpeg")}
        data = {"track_id": "track_no_ext"}
        
        response = client.post("/player/tracks/upload", files=files, data=data)
        
        assert response.status_code == 400
        assert "Tipo de archivo no soportado" in response.json()["detail"]

# Test class for get_track_url endpoint.
class TestGetTrackUrl:
    @patch('controllers.player_controller.supabase')
    def test_get_track_url_audio_found(self, mock_supabase):
        """Test getting URL for an existing audio track."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        
        # Mock list response with matching file
        mock_storage.list.return_value = [{"name": "track_audio.mp3"}]
        mock_storage.get_public_url.return_value = "https://example.com/tracks/track_audio.mp3"
        
        response = client.get("/player/tracks/track_audio")
        
        assert response.status_code == 200
        result = response.json()
        assert result["bucket"] == "tracks"
        assert result["path"] == "track_audio.mp3"
        assert "url" in result
    
    @patch('controllers.player_controller.supabase')
    def test_get_track_url_video_found(self, mock_supabase):
        """Test getting URL for an existing video track."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        
        # Mock list response - audio not found, video found
        def list_side_effect(path, options):
            # First call for tracks bucket returns empty
            if mock_storage.list.call_count == 1:
                return []
            # Second call for videos bucket returns video file
            return [{"name": "track_video.mp4"}]
        
        mock_storage.list.side_effect = list_side_effect
        mock_storage.get_public_url.return_value = "https://example.com/videos/track_video.mp4"
        
        response = client.get("/player/tracks/track_video")
        
        assert response.status_code == 200
        result = response.json()
        assert result["bucket"] == "videos"
        assert result["path"] == "track_video.mp4"
    
    @patch('controllers.player_controller.supabase')
    def test_get_track_url_not_found(self, mock_supabase):
        """Test getting URL for a non-existent track."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        
        # Mock list response - no files found
        mock_storage.list.return_value = []
        
        response = client.get("/player/tracks/nonexistent")
        
        assert response.status_code == 404
        assert "No se encontró ningún archivo" in response.json()["detail"]
    
    @patch('controllers.player_controller.supabase')
    def test_get_track_url_audio_exception(self, mock_supabase):
        """Test handling exception when checking audio tracks."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        
        # First call raises exception (audio check)
        # Second call returns empty list (video check)
        mock_storage.list.side_effect = [Exception("Storage error"), []]
        
        response = client.get("/player/tracks/track_error")
        
        assert response.status_code == 404
    
    @patch('controllers.player_controller.supabase')
    def test_get_track_url_video_mov(self, mock_supabase):
        """Test getting URL for a MOV video."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        
        # Audio not found, video found with .mov extension
        mock_storage.list.side_effect = [
            [],  # tracks bucket
            [{"name": "track_mov.mov"}]  # videos bucket
        ]
        mock_storage.get_public_url.return_value = "https://example.com/videos/track_mov.mov"
        
        response = client.get("/player/tracks/track_mov")
        
        assert response.status_code == 200
        result = response.json()
        assert result["path"] == "track_mov.mov"
    
    @patch('controllers.player_controller.supabase')
    def test_get_track_url_video_avi(self, mock_supabase):
        """Test getting URL for an AVI video."""
        # Setup mock
        mock_storage = Mock()
        mock_supabase.storage.from_.return_value = mock_storage
        
        # Audio not found, video found with .avi extension
        mock_storage.list.side_effect = [
            [],  # tracks bucket
            [{"name": "track_avi.avi"}]  # videos bucket
        ]
        mock_storage.get_public_url.return_value = "https://example.com/videos/track_avi.avi"
        
        response = client.get("/player/tracks/track_avi")
        
        assert response.status_code == 200
        result = response.json()
        assert result["path"] == "track_avi.avi"

