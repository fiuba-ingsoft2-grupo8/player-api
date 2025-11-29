# Imports.
import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Set environment variables before importing any application modules.
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key"

# Mock the supabase module before any imports.
sys.modules['supabase'] = MagicMock()

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# Test class for get_supabase function.
class TestGetSupabase:
    @patch('supabase_client.settings')
    @patch('supabase_client.create_client')
    def test_get_supabase_success(self, mock_create_client, mock_settings):
        """Test that get_supabase creates a client successfully."""
        # Setup mock
        mock_settings.supabase_url = "https://test.supabase.co"
        mock_settings.supabase_service_role_key = "test-key-123"
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        from supabase_client import get_supabase
        
        result = get_supabase()
        
        assert result == mock_client
        mock_create_client.assert_called_once_with(
            "https://test.supabase.co",
            "test-key-123"
        )
    
    @patch('supabase_client.settings')
    def test_get_supabase_missing_url(self, mock_settings):
        """Test that get_supabase raises error when URL is missing."""
        # Setup mock with empty URL
        mock_settings.supabase_url = ""
        mock_settings.supabase_service_role_key = "test-key-123"
        
        from supabase_client import get_supabase
        
        with pytest.raises(RuntimeError) as exc_info:
            get_supabase()
        
        assert "Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY" in str(exc_info.value)
    
    @patch('supabase_client.settings')
    def test_get_supabase_missing_key(self, mock_settings):
        """Test that get_supabase raises error when key is missing."""
        # Setup mock with empty key
        mock_settings.supabase_url = "https://test.supabase.co"
        mock_settings.supabase_service_role_key = ""
        
        from supabase_client import get_supabase
        
        with pytest.raises(RuntimeError) as exc_info:
            get_supabase()
        
        assert "Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY" in str(exc_info.value)
    
    @patch('supabase_client.settings')
    def test_get_supabase_missing_both(self, mock_settings):
        """Test that get_supabase raises error when both URL and key are missing."""
        # Setup mock with both empty
        mock_settings.supabase_url = ""
        mock_settings.supabase_service_role_key = ""
        
        from supabase_client import get_supabase
        
        with pytest.raises(RuntimeError) as exc_info:
            get_supabase()
        
        assert "Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY" in str(exc_info.value)
    
    @patch('supabase_client.settings')
    def test_get_supabase_none_url(self, mock_settings):
        """Test that get_supabase raises error when URL is None."""
        # Setup mock with None URL
        mock_settings.supabase_url = None
        mock_settings.supabase_service_role_key = "test-key-123"
        
        from supabase_client import get_supabase
        
        with pytest.raises(RuntimeError) as exc_info:
            get_supabase()
        
        assert "Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY" in str(exc_info.value)
    
    @patch('supabase_client.settings')
    def test_get_supabase_none_key(self, mock_settings):
        """Test that get_supabase raises error when key is None."""
        # Setup mock with None key
        mock_settings.supabase_url = "https://test.supabase.co"
        mock_settings.supabase_service_role_key = None
        
        from supabase_client import get_supabase
        
        with pytest.raises(RuntimeError) as exc_info:
            get_supabase()
        
        assert "Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY" in str(exc_info.value)

