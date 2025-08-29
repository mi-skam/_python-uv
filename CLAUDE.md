# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python Flask template demonstrating modern development practices with:
- **Flask web framework** with PostgreSQL database integration
- **uv dependency management** for fast package handling
- **Docker containerization** with multi-stage builds
- **just task automation** for streamlined workflows  
- **SQLAlchemy ORM** with automatic request logging
- **Comprehensive testing** with pytest and coverage
- **Quality assurance** with ruff linting and mypy type checking

## Environment Setup

1. **Copy environment template**: `cp .env.example .env`
2. **Configure settings** in `.env` (required - fail-fast approach)
3. **Python version**: 3.12 (specified in pyproject.toml)

## Key Commands

### Development Workflow
```bash
just install          # Install dependencies using uv
just dev              # Start Flask app + PostgreSQL (port 8098)
just req [path]       # Send HTTP request to running server
just browser          # Open development server in browser
```

### Quality Assurance
```bash
just test             # Run tests with pytest
just cov              # Run tests with coverage reporting  
just lint             # Run ruff linter and formatter
just typing           # Run mypy type checking
just check-all        # Run all quality checks (lint + coverage + typing)
```

### Production & Deployment  
```bash
just prod             # Run production server with gunicorn
just prod-container   # Build and run production Docker container
just build-container  # Build multi-platform Docker image
```

### Lifecycle Management
```bash
just update           # Update Python dependencies
just fresh            # Clean install from scratch  
just clear            # Remove temporary files and caches
```

## Configuration

Required environment variables in `.env`:
- **SERVICE_NAME**: python-uv (application identifier)
- **PORT**: Application port (8098)
- **FLASK_ENV**: development or production
- **POSTGRES_USER/PASSWORD/DB/HOST/PORT**: Database connection settings
- **_UV_RUN_ARGS_TEST**: Optional test runner args
- **_UV_RUN_ARGS_SERVE**: Optional server runner args

## Project Structure

```
.
├── src/
│   └── python_example/
│       ├── __init__.py
│       ├── app.py          # Flask application with database integration
│       ├── models.py       # SQLAlchemy database models
│       └── wsgi.py         # WSGI entry point for production
├── tests/
│   ├── __init__.py
│   └── test_main.py        # Test suite
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline
├── .env.example            # Environment template
├── compose.yml             # Docker Compose config
├── compose.prod.yml        # Production Docker config
├── Dockerfile              # Container definition
├── docker-entrypoint.sh    # Container entry point
├── justfile                # Task automation
├── pyproject.toml          # Dependencies and config
├── ruff.toml               # Linter config
├── mypy.ini                # Type checker config
└── uv.lock                 # Locked dependencies
```

## Flask Application

The app (`src/python_example/app.py`) demonstrates database integration:
- `/` - System info with request logging to PostgreSQL database
- `/health` - Health check endpoint  
- `/echo/<text>` - Echo service with text reversal and length

**Key Features:**
- **Database persistence** - All requests are logged to PostgreSQL
- **Automatic schema creation** - Tables created via SQLAlchemy metadata
- **Error handling** - Graceful degradation if database unavailable
- **Request history** - Shows last 10 requests from database

## Testing

```bash
just test         # Run all tests
just cov          # Run tests with coverage report
just check-all    # Run all checks (lint, coverage, typing)
```

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):
- Runs on push/PR to main branch
- Uses Python 3.12
- Executes `just check-all` for quality gates
- Builds and tests Docker container

## Common Issues

### Missing Environment Variables
```
error: environment variable `VARIABLE_NAME` not present
```
**Solution**: Ensure `.env` file exists with all required variables from `.env.example`

### Port Already in Use
```bash
PORT=8099 just dev  # Use alternative port via environment variable
```

### Database Connection Issues
```bash
# Restart database container
docker compose down
just dev  # Will restart PostgreSQL automatically

# Clear database volumes if needed
docker compose down -v
just dev  # Creates fresh database
```

## Best Practices

1. **Always use `.env`**: No hardcoded configuration (fail-fast approach)
2. **Test locally first**: Use `just dev` for development
3. **Run checks**: Use `just check-all` before committing
4. **CI/CD**: All PRs must pass `just check-all` to merge

## Docker

### Build and Run
```bash
just build-container                    # Build Docker image
docker run -p 8080:8080 -e PORT=8080 \
  $(cat .env | xargs) SERVICE_NAME:GIT_ID  # Run container
```

### Production Deployment
```bash
docker compose -f compose.prod.yml up   # Run with production config
```

## Development Workflow

1. Make changes to code
2. Run `just test` to verify tests pass
3. Run `just check-all` to ensure code quality
4. Commit changes (CI will run automatically)

## Justfile Syntax Reference

**IMPORTANT**: Always use proper justfile syntax to avoid errors:

```just
# Variables (at top of file)
var := "value"
var := `command`
var := env_var("VAR_NAME")

# Simple recipe (single command)
target:
    command args

# Recipe with parameters
target param="default":
    command {{param}}

# Recipe with environment variable
target:
    VAR=value command

# Recipe with bash script (for complex logic)
target:
    #!/usr/bin/env bash
    if [ condition ]; then
        command
    fi
```

**Common Mistakes to Avoid:**
- ❌ `target: command` (missing indentation)
- ❌ `target: VAR=value command` (env var on same line)
- ❌ Single-line conditionals with `{{ if }}`
- ✅ Always indent recipe bodies with 4 spaces
- ✅ Put environment variables on separate line
- ✅ Use bash scripts for conditionals