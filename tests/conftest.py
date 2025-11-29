# Imports.
import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, MagicMock

# Set environment variables before importing any application modules.
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key"

# Mock the supabase module before any imports.
sys.modules['supabase'] = MagicMock()

# Add the src directory to sys.path to import application modules.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# Now import the application modules.
from main import app
import repositories as repo

# Replace the actual supabase client with a mock.
repo.sb = MagicMock()

# Define pytest fixtures.
@pytest.fixture()
def client():
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client

# Fixture to provide access to the mocked Supabase client.
@pytest.fixture()
def mock_sb():
    """Provide access to the mocked Supabase client for tests."""
    return repo.sb
