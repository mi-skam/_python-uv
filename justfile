# justfile for python-docker-uv project

# Load environment variables from .env file
set dotenv-load := true

SERVICE_NAME := env_var("SERVICE_NAME")
PORT := env_var("PORT")
GIT_USER := env_var("GIT_USER")
GIT_REGISTRY := env_var("GIT_REGISTRY")
GIT_HASH := `git rev-parse --short HEAD`
GIT_REPO := `basename $(git rev-parse --show-toplevel)`

HOST := env("HOST", "127.0.0.1")
ARGS_TEST := env("_UV_RUN_ARGS_TEST", "")
ARGS_SERVE := env("_UV_RUN_ARGS_SERVE", "")

# Show available commands
@_:
    @just --list --unsorted

# Run tests
[group('qa')]
test *args:
    uv run {{ ARGS_TEST }} -m pytest {{ args }}

_cov *args:
    uv run -m coverage {{ args }}

# Run tests and measure coverage
[group('qa')]
@cov *args:
    just _cov erase
    just _cov run -m pytest tests
    just _cov report
    just _cov html

# Run linters
[group('qa')]
lint:
    uv run ruff check
    uv run ruff format

# Check types
[group('qa')]
typing:
    uv run ty check src .venv

# Perform all checks
[group('qa')]
check-all: lint cov typing

# Test deployment locally with git hash
[group('qa')]
test-deploy: push-container
    IMAGE_TAG={{GIT_HASH}} GIT_REGISTRY={{GIT_REGISTRY}} GIT_USER={{GIT_USER}} GIT_REPO={{GIT_REPO}} docker compose -f compose.prod.yml up --remove-orphans -d

# Run development server
[group('run')]
dev:
    #!/usr/bin/env bash
    # Start Docker Compose services if compose.yml exists
    if [ -f compose.yml ]; then
        echo "Starting Docker Compose services..."
        docker compose -f compose.yml up --remove-orphans -d
        echo "Waiting for services to be ready..."
        sleep 3
    fi

    FLASK_ENV=development uv run {{ ARGS_SERVE }} flask --app python_example.app:app run --debug --port={{ PORT }}
# Run production server with gunicorn
[group('run')]
prod:
    #!/usr/bin/env bash
    if [ -f compose.yml ]; then
        echo "Starting Docker Compose services..."
        docker compose -f compose.yml up --remove-orphans -d
        echo "Waiting for services to be ready..."
        sleep 3
    fi
    FLASK_ENV=production uv run gunicorn python_example.wsgi:app --bind 0.0.0.0:{{ PORT }} --workers 4

[group('run')]
prod-container: build-container
    docker compose -f compose.prod.yml up --remove-orphans --build

_http *args:
    uv run http {{ args }}

# Send HTTP request to development server
[group('run')]
req path="" *args:
    @just _http {{ args }} http://{{HOST}}:{{ PORT }}/{{ path }}

# Open development server in web browser
[group('run')]
browser:
    uv run -m webbrowser -t http://{{HOST}}:{{ PORT }}

# Update dependencies
[group('lifecycle')]
update:
    uv sync --upgrade

# Ensure project virtualenv is up to date
[group('lifecycle')]
install:
    uv sync

# Remove temporary files
[group('lifecycle')]
clear:
    rm -rf .venv .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
    find . -type d -name "__pycache__" -exec rm -r {} +

# Recreate project virtualenv from nothing
[group('lifecycle')]
fresh: clear install

# Build Docker image if not exists or if dependencies changed (defaults to host platform for speed)
[group('deploy')]
build-container:
    docker buildx build --platform linux/amd64,linux/arm64 -t {{GIT_REPO}}:latest .

[group('deploy')]
push-container: build-container
    #!/usr/bin/env bash
    docker tag {{GIT_REPO}}:latest {{GIT_REGISTRY}}/{{GIT_USER}}/{{GIT_REPO}}:latest
    docker tag {{GIT_REPO}}:latest {{GIT_REGISTRY}}/{{GIT_USER}}/{{GIT_REPO}}:{{GIT_HASH}}
    docker push {{GIT_REGISTRY}}/{{GIT_USER}}/{{GIT_REPO}}:latest
    docker push {{GIT_REGISTRY}}/{{GIT_USER}}/{{GIT_REPO}}:{{GIT_HASH}}

    