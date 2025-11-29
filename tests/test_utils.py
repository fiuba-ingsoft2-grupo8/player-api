# Imports.
import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch

# Set environment variables before importing any application modules.
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key"
os.environ["AUDIO_BUCKET"] = "audio"
os.environ["IMAGES_BUCKET"] = "images"
os.environ["SIGNED_URL_TTL"] = "3600"

# Mock the supabase module before any imports.
sys.modules['supabase'] = MagicMock()

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import _normalize_object_path, signed_download_url, make_audio_url, make_image_url

# Test class for _normalize_object_path function.
class TestNormalizeObjectPath:
    def test_normalize_empty_path(self):
        """Test normalizing an empty path returns None."""
        result = _normalize_object_path("audio", "")
        assert result is None
    
    def test_normalize_none_path(self):
        """Test normalizing None path returns None."""
        result = _normalize_object_path("audio", None)
        assert result is None
    
    def test_normalize_whitespace_path(self):
        """Test normalizing whitespace-only path returns empty string."""
        result = _normalize_object_path("audio", "   ")
        assert result == ""
    
    def test_normalize_path_without_bucket_prefix(self):
        """Test normalizing path without bucket prefix."""
        result = _normalize_object_path("audio", "track_123.mp3")
        assert result == "track_123.mp3"
    
    def test_normalize_path_with_bucket_prefix(self):
        """Test normalizing path with bucket prefix removes it."""
        result = _normalize_object_path("audio", "audio/track_123.mp3")
        assert result == "track_123.mp3"
    
    def test_normalize_path_with_leading_slash(self):
        """Test normalizing path with leading slash."""
        result = _normalize_object_path("images", "/cover_123.jpg")
        assert result == "cover_123.jpg"
    
    def test_normalize_path_with_bucket_and_slash(self):
        """Test normalizing path with bucket prefix and leading slash."""
        result = _normalize_object_path("images", "/images/cover_123.jpg")
        assert result == "cover_123.jpg"
    
    def test_normalize_nested_path(self):
        """Test normalizing nested path."""
        result = _normalize_object_path("audio", "audio/artist/album/track.mp3")
        assert result == "artist/album/track.mp3"
    
    def test_normalize_path_wrong_bucket_prefix(self):
        """Test normalizing path with different bucket prefix."""
        result = _normalize_object_path("audio", "images/cover.jpg")
        # Should not remove the prefix since it doesn't match
        assert result == "images/cover.jpg"

# Test class for signed_download_url function.
class TestSignedDownloadUrl:
    @patch('utils.sb')
    def test_signed_download_url_with_signedURL_key(self, mock_sb):
        """Test generating signed URL when response has 'signedURL' key."""
        # Setup mock
        mock_storage = Mock()
        mock_sb.storage.from_.return_value = mock_storage
        mock_storage.create_signed_url.return_value = {
            "signedURL": "https://example.com/signed/audio/track.mp3?token=abc123"
        }
        
        result = signed_download_url("audio", "track.mp3", 7200)
        
        assert result == "https://example.com/signed/audio/track.mp3?token=abc123"
        mock_storage.create_signed_url.assert_called_once_with("track.mp3", 7200)
    
    @patch('utils.sb')
    def test_signed_download_url_with_signed_url_key(self, mock_sb):
        """Test generating signed URL when response has 'signed_url' key."""
        # Setup mock
        mock_storage = Mock()
        mock_sb.storage.from_.return_value = mock_storage
        mock_storage.create_signed_url.return_value = {
            "signed_url": "https://example.com/signed/images/cover.jpg?token=def456"
        }
        
        result = signed_download_url("images", "cover.jpg")
        
        assert result == "https://example.com/signed/images/cover.jpg?token=def456"
    
    @patch('utils.sb')
    def test_signed_download_url_empty_path(self, mock_sb):
        """Test generating signed URL with empty path returns None."""
        result = signed_download_url("audio", "")
        
        assert result is None
    
    @patch('utils.sb')
    def test_signed_download_url_none_path(self, mock_sb):
        """Test generating signed URL with None path returns None."""
        result = signed_download_url("audio", None)
        
        assert result is None
    
    @patch('utils.sb')
    @patch('utils.settings')
    def test_signed_download_url_default_ttl(self, mock_settings, mock_sb):
        """Test generating signed URL uses default TTL from settings."""
        # Setup mock
        mock_settings.signed_url_ttl = 1800
        mock_storage = Mock()
        mock_sb.storage.from_.return_value = mock_storage
        mock_storage.create_signed_url.return_value = {
            "signedURL": "https://example.com/signed/audio/track.mp3"
        }
        
        result = signed_download_url("audio", "track.mp3")
        
        # Should use settings TTL when not provided
        mock_storage.create_signed_url.assert_called_once_with("track.mp3", 1800)
    
    @patch('utils.sb')
    def test_signed_download_url_with_bucket_prefix(self, mock_sb):
        """Test generating signed URL with path containing bucket prefix."""
        # Setup mock
        mock_storage = Mock()
        mock_sb.storage.from_.return_value = mock_storage
        mock_storage.create_signed_url.return_value = {
            "signedURL": "https://example.com/signed/audio/track.mp3"
        }
        
        # Path with bucket prefix should be normalized
        result = signed_download_url("audio", "audio/track.mp3", 3600)
        
        # Should call with normalized path (prefix removed)
        mock_storage.create_signed_url.assert_called_once_with("track.mp3", 3600)
    
    @patch('utils.sb')
    def test_signed_download_url_no_url_in_response(self, mock_sb):
        """Test generating signed URL when response has no URL keys."""
        # Setup mock
        mock_storage = Mock()
        mock_sb.storage.from_.return_value = mock_storage
        mock_storage.create_signed_url.return_value = {}
        
        result = signed_download_url("audio", "track.mp3")
        
        assert result is None

# Test class for make_audio_url function.
class TestMakeAudioUrl:
    @patch('utils.signed_download_url')
    @patch('utils.settings')
    def test_make_audio_url_success(self, mock_settings, mock_signed_url):
        """Test making audio URL successfully."""
        # Setup mock
        mock_settings.audio_bucket = "audio"
        mock_settings.signed_url_ttl = 3600
        mock_signed_url.return_value = "https://example.com/signed/audio/track.mp3"
        
        result = make_audio_url("track.mp3")
        
        assert result == "https://example.com/signed/audio/track.mp3"
        mock_signed_url.assert_called_once_with("audio", "track.mp3", 3600)
    
    @patch('utils.signed_download_url')
    @patch('utils.settings')
    def test_make_audio_url_with_path_prefix(self, mock_settings, mock_signed_url):
        """Test making audio URL with path containing prefix."""
        # Setup mock
        mock_settings.audio_bucket = "audio"
        mock_settings.signed_url_ttl = 3600
        mock_signed_url.return_value = "https://example.com/signed/audio/album/track.mp3"
        
        result = make_audio_url("album/track.mp3")
        
        assert result is not None
        mock_signed_url.assert_called_once()
    
    @patch('utils.signed_download_url')
    @patch('utils.settings')
    def test_make_audio_url_empty_path(self, mock_settings, mock_signed_url):
        """Test making audio URL with empty path."""
        # Setup mock
        mock_settings.audio_bucket = "audio"
        mock_settings.signed_url_ttl = 3600
        mock_signed_url.return_value = None
        
        result = make_audio_url("")
        
        assert result is None

# Test class for make_image_url function.
class TestMakeImageUrl:
    @patch('utils.signed_download_url')
    @patch('utils.settings')
    def test_make_image_url_success(self, mock_settings, mock_signed_url):
        """Test making image URL successfully."""
        # Setup mock
        mock_settings.images_bucket = "images"
        mock_settings.signed_url_ttl = 3600
        mock_signed_url.return_value = "https://example.com/signed/images/cover.jpg"
        
        result = make_image_url("cover.jpg")
        
        assert result == "https://example.com/signed/images/cover.jpg"
        mock_signed_url.assert_called_once_with("images", "cover.jpg", 3600)
    
    @patch('utils.signed_download_url')
    @patch('utils.settings')
    def test_make_image_url_with_path_prefix(self, mock_settings, mock_signed_url):
        """Test making image URL with path containing prefix."""
        # Setup mock
        mock_settings.images_bucket = "images"
        mock_settings.signed_url_ttl = 3600
        mock_signed_url.return_value = "https://example.com/signed/images/artist/cover.jpg"
        
        result = make_image_url("artist/cover.jpg")
        
        assert result is not None
        mock_signed_url.assert_called_once()
    
    @patch('utils.signed_download_url')
    @patch('utils.settings')
    def test_make_image_url_empty_path(self, mock_settings, mock_signed_url):
        """Test making image URL with empty path."""
        # Setup mock
        mock_settings.images_bucket = "images"
        mock_settings.signed_url_ttl = 3600
        mock_signed_url.return_value = None
        
        result = make_image_url("")
        
        assert result is None
    
    @patch('utils.signed_download_url')
    @patch('utils.settings')
    def test_make_image_url_different_formats(self, mock_settings, mock_signed_url):
        """Test making image URL with different image formats."""
        # Setup mock
        mock_settings.images_bucket = "images"
        mock_settings.signed_url_ttl = 3600
        
        # Test PNG
        mock_signed_url.return_value = "https://example.com/signed/images/cover.png"
        result = make_image_url("cover.png")
        assert result is not None
        
        # Test JPEG
        mock_signed_url.return_value = "https://example.com/signed/images/cover.jpeg"
        result = make_image_url("cover.jpeg")
        assert result is not None
        
        # Test WebP
        mock_signed_url.return_value = "https://example.com/signed/images/cover.webp"
        result = make_image_url("cover.webp")
        assert result is not None

