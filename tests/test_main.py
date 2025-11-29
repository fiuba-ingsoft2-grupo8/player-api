# Imports.
import pytest

# Test class for health endpoint.
class TestHealth:
    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {}
