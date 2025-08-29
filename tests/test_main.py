import json
import os
import pytest
from unittest.mock import patch, MagicMock
from src.python_example.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    # Set required environment variables for testing
    os.environ["FLASK_ENV"] = "testing"
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


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


def test_root_endpoint_database_dependent(client):
    """Test the root endpoint - works with database, fails without."""
    response = client.get("/")
    data = json.loads(response.data)
    
    if response.status_code == 200:
        # Database is available - test successful response
        assert "environment" in data
        assert "debug_mode" in data
        assert "flask_version" in data
        assert "python_version" in data
        assert "timestamp" in data
        assert "port" in data
        assert "service_name" in data
        assert "recent_requests" in data
    elif response.status_code == 503:
        # Database is unavailable - test error response
        assert "details" in data
    else:
        # Unexpected status code
        assert False, f"Unexpected status code: {response.status_code}"


@patch("src.python_example.app.get_db_session")
def test_root_endpoint_with_database(mock_db_session, client):
    """Test the root endpoint with mocked database."""
    # Mock database session and query
    mock_session = MagicMock()
    mock_db_session.return_value = mock_session
    
    # Mock query results (empty list of recent requests)
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []
    
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Check expected fields are present
    assert "environment" in data
    assert "debug_mode" in data
    assert "flask_version" in data
    assert "python_version" in data
    assert "timestamp" in data
    assert "port" in data
    assert "service_name" in data
    assert "recent_requests" in data
    assert data["recent_requests"] == []
    
    # Verify database operations were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


@patch("src.python_example.app.get_db_session")
def test_root_endpoint_database_error(mock_db_session, client):
    """Test the root endpoint handles database errors gracefully."""
    # Mock database session to raise an exception
    mock_db_session.side_effect = Exception("Database connection failed")
    
    response = client.get("/")
    assert response.status_code == 503
    data = json.loads(response.data)
    assert "details" in data
    assert "Database connection failed" in data["details"]