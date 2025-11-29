# Imports.
import pytest
import os
import sys
from unittest.mock import patch

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# Test class for Settings configuration.
class TestSettings:
    @patch.dict(os.environ, {
        "APP_ENV": "production",
        "ALLOWED_ORIGINS": "https://example.com,https://app.example.com",
        "SUPABASE_URL": "https://myproject.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "super-secret-key-123",
        "AUDIO_BUCKET": "audio-files",
        "IMAGES_BUCKET": "image-files",
        "SIGNED_URL_TTL": "7200"
    })
    def test_settings_with_custom_env_vars(self):
        """Test that settings load custom environment variables correctly."""
        # Import fresh to get new env vars
        import importlib
        import config
        importlib.reload(config)
        
        settings = config.Settings()
        
        assert settings.app_env == "production"
        assert settings.allowed_origins == "https://example.com,https://app.example.com"
        assert settings.supabase_url == "https://myproject.supabase.co"
        assert settings.supabase_service_role_key == "super-secret-key-123"
        assert settings.audio_bucket == "audio-files"
        assert settings.images_bucket == "image-files"
        assert settings.signed_url_ttl == 7200
    
    @patch.dict(os.environ, {}, clear=True)
    def test_settings_with_default_values(self):
        """Test that settings use default values when env vars are not set."""
        # Import fresh
        import importlib
        import config
        importlib.reload(config)
        
        settings = config.Settings()
        
        assert settings.app_env == "development"
        assert settings.allowed_origins == "*"
        assert settings.supabase_url == ""
        assert settings.supabase_service_role_key == ""
        assert settings.audio_bucket == "audio"
        assert settings.images_bucket == "images"
        assert settings.signed_url_ttl == 3600
    
    @patch.dict(os.environ, {
        "APP_ENV": "staging",
        "ALLOWED_ORIGINS": ""
    })
    def test_settings_with_empty_allowed_origins(self):
        """Test that settings handle empty ALLOWED_ORIGINS."""
        # Import fresh
        import importlib
        import config
        importlib.reload(config)
        
        settings = config.Settings()
        
        assert settings.allowed_origins == ""
    
    @patch.dict(os.environ, {
        "SIGNED_URL_TTL": "invalid"
    })
    def test_settings_with_invalid_ttl(self):
        """Test that settings handle invalid TTL value."""
        # Import fresh
        import importlib
        import config
        
        # This should raise ValueError when trying to convert "invalid" to int
        with pytest.raises(ValueError):
            importlib.reload(config)
            config.Settings()
    
    @patch.dict(os.environ, {
        "SIGNED_URL_TTL": "0"
    })
    def test_settings_with_zero_ttl(self):
        """Test that settings accept zero TTL."""
        # Import fresh
        import importlib
        import config
        importlib.reload(config)
        
        settings = config.Settings()
        
        assert settings.signed_url_ttl == 0
    
    @patch.dict(os.environ, {
        "SIGNED_URL_TTL": "-100"
    })
    def test_settings_with_negative_ttl(self):
        """Test that settings accept negative TTL."""
        # Import fresh
        import importlib
        import config
        importlib.reload(config)
        
        settings = config.Settings()
        
        assert settings.signed_url_ttl == -100
    
    @patch.dict(os.environ, {
        "APP_ENV": "test",
        "SUPABASE_URL": "http://localhost:54321"
    })
    def test_settings_partial_override(self):
        """Test that settings can partially override defaults."""
        # Import fresh
        import importlib
        import config
        importlib.reload(config)
        
        settings = config.Settings()
        
        assert settings.app_env == "test"
        assert settings.supabase_url == "http://localhost:54321"
        # Others should be defaults
        assert settings.audio_bucket == "audio"
        assert settings.images_bucket == "images"

