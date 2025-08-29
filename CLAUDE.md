# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask application with uv dependency management and Docker containerization. Uses `just` for task automation.

## Environment Setup

1. **Copy environment template**: `cp .env.example .env`
2. **Configure settings** in `.env` (required - no defaults)
3. **Python version**: 3.12 (specified in pyproject.toml)

## Key Commands

```bash
# Development
just serve            # Start development server
just prod             # Run production server with gunicorn
just req [path]       # Send HTTP request to development server
just browser          # Open development server in browser

# Testing & Quality
just test             # Run tests with pytest
just cov              # Run tests with coverage
just lint             # Run linters (ruff)
just typing           # Check types
just check-all        # Run all checks (lint, coverage, typing)

# Lifecycle
just install          # Install dependencies
just update           # Update dependencies
just fresh            # Clean install from scratch
just clear            # Remove temporary files
just build-container  # Build Docker image
```

## Configuration

Required environment variables in `.env`:
- **SERVICE_NAME**: python-docker-uv
- **PORT**: Application port (8098)
- **_UV_RUN_ARGS_TEST**: Optional test runner args
- **_UV_RUN_ARGS_SERVE**: Optional server runner args

## Project Structure

```
.
├── src/
│   └── python_example/
│       ├── __init__.py
│       └── app.py          # Flask application
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

The app (`src/python_example/app.py`) provides three endpoints:
- `/` - System info with timestamp, Python version, and deployment info
- `/health` - Health check endpoint
- `/echo/<text>` - Echo service with text reversal and length

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
PORT=8099 just serve  # Use alternative port via environment variable
```

## Best Practices

1. **Always use `.env`**: No hardcoded configuration (fail-fast approach)
2. **Test locally first**: Use `just serve` for development
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