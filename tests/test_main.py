import json

import pytest

from src.python_example.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "running"
    assert "environment" in data
    assert "debug_mode" in data
    assert "flask_version" in data
    assert "python_version" in data
    assert "timestamp" in data
    assert "port" in data
    assert "service_name" in data
    assert data["deployed_with"] == "uv + Docker"


def test_echo_endpoint(client):
    """Test the echo endpoint."""
    test_text = "hello"
    response = client.get(f"/echo/{test_text}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["you_said"] == test_text
    assert data["reversed"] == test_text[::-1]
    assert data["length"] == len(test_text)


def test_echo_endpoint_empty_string(client):
    """Test the echo endpoint with empty string."""
    response = client.get("/echo/")
    assert response.status_code == 404  # Flask returns 404 for empty path parameter


def test_echo_endpoint_special_characters(client):
    """Test the echo endpoint with special characters."""
    test_text = "hello-world_123"
    response = client.get(f"/echo/{test_text}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["you_said"] == test_text
    assert data["reversed"] == test_text[::-1]
    assert data["length"] == len(test_text)
