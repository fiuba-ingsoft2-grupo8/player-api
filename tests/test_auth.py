# Imports.
import pytest
import os
import sys
from unittest.mock import patch, MagicMock
import jwt

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from auth import verify_token, is_testing

# Test class for is_testing function.
class TestIsTesting:
    def test_is_testing_in_pytest(self):
        """Test that is_testing returns True when running in pytest."""
        assert is_testing() == True
    
    def test_is_testing_with_env_var(self):
        """Test that is_testing returns True when TESTING env var is set."""
        with patch.dict(os.environ, {"TESTING": "true"}):
            assert is_testing() == True

# Test class for verify_token function.
class TestVerifyToken:
    def test_verify_token_in_testing_mode(self):
        """Test that verify_token returns test user data during testing."""
        result = verify_token()
        assert result["user_id"] == "test_user_123"
        assert result["email"] == "test@example.com"
        assert result["user_type"] == "user"
    
    @patch('auth.is_testing')
    def test_verify_token_no_authorization_header(self, mock_is_testing):
        """Test that missing authorization header raises 401 error."""
        mock_is_testing.return_value = False
        
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            verify_token(authorization=None)
        
        assert exc_info.value.status_code == 401
        assert "Authorization header required" in str(exc_info.value.detail)
    
    @patch('auth.is_testing')
    def test_verify_token_invalid_format_single_part(self, mock_is_testing):
        """Test that invalid authorization format raises 401 error."""
        mock_is_testing.return_value = False
        
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            verify_token(authorization="InvalidToken")
        
        assert exc_info.value.status_code == 401
        assert "Authorization header must be in format" in str(exc_info.value.detail)
    
    @patch('auth.is_testing')
    def test_verify_token_invalid_format_wrong_scheme(self, mock_is_testing):
        """Test that non-Bearer scheme raises 401 error."""
        mock_is_testing.return_value = False
        
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            verify_token(authorization="Basic sometoken")
        
        assert exc_info.value.status_code == 401
        assert "Authorization header must be in format" in str(exc_info.value.detail)
    
    @patch('auth.is_testing')
    @patch('auth.JWT_SECRET', 'test-secret-key')
    def test_verify_token_valid_token(self, mock_is_testing):
        """Test that valid token is decoded successfully."""
        mock_is_testing.return_value = False
        
        # Create a valid token
        payload = {
            "user_id": "user_456",
            "email": "real@example.com",
            "user_type": "admin"
        }
        token = jwt.encode(payload, 'test-secret-key', algorithm="HS256")
        
        result = verify_token(authorization=f"Bearer {token}")
        assert result["user_id"] == "user_456"
        assert result["email"] == "real@example.com"
        assert result["user_type"] == "admin"
    
    @patch('auth.is_testing')
    @patch('auth.JWT_SECRET', 'test-secret-key')
    def test_verify_token_expired_token(self, mock_is_testing):
        """Test that expired token raises 401 error."""
        mock_is_testing.return_value = False
        
        from fastapi import HTTPException
        import time
        
        # Create an expired token
        payload = {
            "user_id": "user_789",
            "exp": int(time.time()) - 3600  # Expired 1 hour ago
        }
        token = jwt.encode(payload, 'test-secret-key', algorithm="HS256")
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(authorization=f"Bearer {token}")
        
        assert exc_info.value.status_code == 401
        assert "Token has expired" in str(exc_info.value.detail)
    
    @patch('auth.is_testing')
    @patch('auth.JWT_SECRET', 'test-secret-key')
    def test_verify_token_invalid_signature(self, mock_is_testing):
        """Test that token with invalid signature raises 401 error."""
        mock_is_testing.return_value = False
        
        from fastapi import HTTPException
        
        # Create token with wrong secret
        payload = {"user_id": "user_999"}
        token = jwt.encode(payload, 'wrong-secret', algorithm="HS256")
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(authorization=f"Bearer {token}")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)
    
    @patch('auth.is_testing')
    def test_verify_token_malformed_token(self, mock_is_testing):
        """Test that malformed token raises 401 error."""
        mock_is_testing.return_value = False
        
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(authorization="Bearer not-a-valid-jwt")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)

