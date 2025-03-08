"""
Tests for the main application endpoints.

This module contains tests for the main API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)

def test_read_main():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ISMS API is running"}

def test_read_users():
    """Test the users endpoint."""
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_read_assets():
    """Test the assets endpoint."""
    response = client.get("/api/assets/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_read_risks():
    """Test the risks endpoint."""
    response = client.get("/api/risks/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_read_policies():
    """Test the policies endpoint."""
    response = client.get("/api/policies/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_read_incidents():
    """Test the incidents endpoint."""
    response = client.get("/api/incidents/")
    assert response.status_code == 200
    assert "message" in response.json()