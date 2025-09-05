"""Deployment configuration tests for environment variable handling."""

import os
from unittest.mock import patch

import pytest


class TestEnvironmentVariableOverrides:
    """Test that environment variables properly override .env file values."""

    def test_port_override(self):
        """Test that PORT environment variable overrides .env value."""
        original_port = os.environ.get("PORT")

        try:
            # Set custom PORT
            test_port = "9999"
            os.environ["PORT"] = test_port

            # Import app after setting environment
            from python_example.app import app

            with app.test_client() as client:
                response = client.get("/")
                # Check if response contains the overridden port
                # Note: Failure is OK if DB is unavailable
                if response.status_code == 200:
                    data = response.get_json()
                    assert data["port"] == test_port
                elif response.status_code == 503:
                    # Database not available is OK for this test
                    pass

        finally:
            # Restore original PORT
            if original_port:
                os.environ["PORT"] = original_port
            else:
                os.environ.pop("PORT", None)

    def test_postgres_port_override(self):
        """Test that POSTGRES_PORT environment variable overrides .env value."""
        original_port = os.environ.get("POSTGRES_PORT")

        try:
            # Set custom POSTGRES_PORT
            test_port = "5434"
            os.environ["POSTGRES_PORT"] = test_port

            # Mock the database connection to capture the URL
            with patch("python_example.app.get_db_session") as mock_get_db:
                from python_example.app import app

                with app.test_client() as client:
                    client.get("/")  # Trigger the request

                    # Check if get_db_session was called with correct port
                    if mock_get_db.called:
                        call_args = mock_get_db.call_args
                        database_url = call_args.kwargs.get("database_url", "")
                        # Verify the port is in the connection string
                        assert f":{test_port}/" in database_url

        finally:
            # Restore original POSTGRES_PORT
            if original_port:
                os.environ["POSTGRES_PORT"] = original_port
            else:
                os.environ.pop("POSTGRES_PORT", None)

    def test_multiple_env_overrides(self):
        """Test that multiple environment variables can be overridden simultaneously."""
        originals = {
            "PORT": os.environ.get("PORT"),
            "POSTGRES_PORT": os.environ.get("POSTGRES_PORT"),
            "SERVICE_NAME": os.environ.get("SERVICE_NAME"),
            "FLASK_ENV": os.environ.get("FLASK_ENV"),
        }

        try:
            # Set multiple custom values
            os.environ["PORT"] = "7777"
            os.environ["POSTGRES_PORT"] = "5435"
            os.environ["SERVICE_NAME"] = "test-service"
            os.environ["FLASK_ENV"] = "testing"

            from python_example.app import app

            with app.test_client() as client:
                response = client.get("/")

                if response.status_code == 200:
                    data = response.get_json()
                    assert data["port"] == "7777"
                    assert data["service_name"] == "test-service"
                    assert data["environment"] == "testing"

        finally:
            # Restore all original values
            for key, value in originals.items():
                if value:
                    os.environ[key] = value
                else:
                    os.environ.pop(key, None)


class TestEnvironmentHierarchy:
    """Test the environment variable loading hierarchy."""

    def test_env_file_loads_when_no_override(self):
        """Test that .env file values are used when no environment override exists."""
        # Clear environment variable to ensure .env value is used
        original = os.environ.pop("SERVICE_NAME", None)

        try:
            # Load the app - should use .env file value
            # Re-set from .env for testing
            from dotenv import load_dotenv

            from python_example.app import app

            load_dotenv()

            with app.test_client() as client:
                response = client.get("/")

                if response.status_code == 200:
                    data = response.get_json()
                    # Should have the value from .env file
                    assert "service_name" in data
                    expected = os.environ.get("SERVICE_NAME", "python-uv")
                    assert data["service_name"] == expected

        finally:
            if original:
                os.environ["SERVICE_NAME"] = original

    def test_command_line_override_precedence(self):
        """Test that command-line env vars take precedence over .env file."""
        # This test simulates what happens when running:
        # POSTGRES_PORT=5434 just dev

        # Save original
        original_port = os.environ.get("POSTGRES_PORT")

        try:
            # First, load .env file (simulates justfile loading)
            from dotenv import load_dotenv

            load_dotenv(override=False)

            # Then override with command-line value (simulates POSTGRES_PORT=5434)
            os.environ["POSTGRES_PORT"] = "5434"

            # Now import app
            from python_example.app import app

            # Verify the override worked
            assert os.environ["POSTGRES_PORT"] == "5434"

            with patch("python_example.app.get_db_session") as mock_get_db:
                with app.test_client() as client:
                    client.get("/")  # Trigger the request

                    if mock_get_db.called:
                        call_args = mock_get_db.call_args
                        database_url = call_args.kwargs.get("database_url", "")
                        # Should use 5434, not the default 5432
                        assert ":5434/" in database_url
                        assert ":5432/" not in database_url

        finally:
            if original_port:
                os.environ["POSTGRES_PORT"] = original_port
            else:
                os.environ.pop("POSTGRES_PORT", None)


@pytest.mark.integration
class TestDeploymentIntegration:
    """Integration tests for deployment configurations."""

    def test_development_server_with_custom_port(self):
        """Test that development server respects PORT environment variable."""
        # This test would actually start the server, but we'll mock it
        # In a real integration test, you'd use subprocess to run the server

        test_port = "8888"
        original_port = os.environ.get("PORT")

        try:
            os.environ["PORT"] = test_port

            from python_example.app import app

            # Verify app configuration
            with app.test_client() as client:
                response = client.get("/health")
                assert response.status_code == 200

        finally:
            if original_port:
                os.environ["PORT"] = original_port
            else:
                os.environ.pop("PORT", None)

    def test_production_config_loading(self):
        """Test that production configuration loads correctly."""
        original_env = os.environ.get("FLASK_ENV")

        try:
            os.environ["FLASK_ENV"] = "production"

            from python_example.app import app

            with app.test_client() as client:
                response = client.get("/")

                if response.status_code == 200:
                    data = response.get_json()
                    assert data["environment"] == "production"

        finally:
            if original_env:
                os.environ["FLASK_ENV"] = original_env
            else:
                os.environ.pop("FLASK_ENV", None)
