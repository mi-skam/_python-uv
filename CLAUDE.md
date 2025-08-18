# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask application with uv dependency management designed for containerized deployment. The project uses `just` for task automation, Docker Compose for development, and supports multiple Python versions through `.python-version`.

## Environment Setup

1. **Copy the environment template**: `cp .env.example .env`
2. **Configure your settings** in `.env` (required for all commands)
3. **Python version** is controlled by `.python-version` file (currently 3.12)

## Key Commands

### Development
```bash
just dev [port]       # Start development server with Docker Compose watch mode (default: 8082)
just test-prod [port] # Test production build locally
just update           # Update dependencies using dockerized uv
```

### Build
```bash
just build [platform] # Build Docker image (defaults to host platform)
```

### Maintenance
```bash
just clean            # Clean up Docker images
```

## Architecture

### Configuration Management
All configuration is managed through environment variables in `.env`:
- **SERVICE_NAME**: Application service name (python-uv-app)
- **PORT**: Application port (8080)
- **DEV_LOCAL_PORT**: Local development port (8082)
- **PYTHON_IMAGE**: Auto-derived from `.python-version`

### Python Version Management
- **Single source of truth**: `.python-version` file
- **Automatic image derivation**: `python:X.Y-slim`
- **Tested versions**: 3.9, 3.11, 3.12
- **Change version**: `echo "3.13" > .python-version`

### Docker Build Strategy
- **Platform flexibility**: 
  - `just build` - Uses host platform (fast local builds)
  - `just build linux/amd64` - For x86_64 servers
- **Multi-stage builds** with uv for fast dependency installation
- **Security**: Runs as non-root user (appuser)

### Development Workflow
- **Docker Compose with watch mode**: Auto-syncs file changes
- **No local dependencies**: Everything runs in containers
- **Dockerized uv**: No need for local uv installation

### Flask Application
- `main.py`: Simple Flask app with three endpoints
  - `/` - Returns JSON with timestamp and Python version
  - `/health` - Health check endpoint
  - `/echo/<text>` - Echo service for testing
- Configurable via environment variables
- Production-ready with Gunicorn

## Common Issues and Solutions

### Missing Environment Variables
```bash
error: environment variable `VARIABLE_NAME` not present
```
**Solution**: Ensure `.env` file exists with all required variables

### Port Already in Use
```bash
just dev 8083  # Use alternative port
```

## Testing Python Version Changes

1. **Change Python version**:
   ```bash
   echo "3.11" > .python-version
   ```

2. **Build and test locally**:
   ```bash
   just build
   just test-prod
   ```

## Best Practices

1. **Always use `.env`**: No hardcoded configuration
2. **Test locally first**: Use `just dev` for development
3. **Version control**: `.env` is gitignored, `.env.example` is tracked

## Security Notes

- `.env` file is gitignored (never commit secrets)
- Docker containers run as non-root user
- All secrets should be environment variables

## Project Structure

```
.
├── .env.example        # Environment template (tracked)
├── .env               # Local configuration (gitignored)
├── .python-version    # Python version specification
├── compose.yml        # Docker Compose configuration
├── Dockerfile         # Multi-stage build with uv
├── justfile          # Task automation
├── main.py           # Flask application
├── pyproject.toml    # Python dependencies
└── uv.lock          # Locked dependencies
```

## Design Patterns Used

- **Configuration as Code**: All settings in `.env`
- **Single Source of Truth**: `.python-version` for Python version