# Python Flask Template with uv & Docker

A production-ready Flask application template demonstrating modern Python development practices with containerization, dependency management, and database integration.

## Template Overview

- **Flask web framework** with PostgreSQL database integration
- **uv dependency management** for fast, reliable package handling  
- **Docker containerization** with multi-stage builds for production deployment
- **just task automation** for streamlined development workflows
- **Database models & migrations** using SQLAlchemy ORM
- **Quality assurance tools** including linting, testing, and type checking
- **GitHub Actions CI/CD** pipeline ready for deployment

## Architecture Components

### Core Application (`src/python_example/`)
- **`app.py`** - Main Flask application with request logging to database
- **`models.py`** - SQLAlchemy models for data persistence 
- **`wsgi.py`** - WSGI entry point for production deployment

### Development Infrastructure
- **`justfile`** - Task automation (like `npm scripts` but more powerful)
- **`pyproject.toml`** - Project dependencies and Python package configuration
- **`uv.lock`** - Locked dependency versions for reproducible builds
- **`compose.yml`** - PostgreSQL database for local development

### Production Infrastructure  
- **`Dockerfile`** - Multi-stage build optimized for production
- **`compose.prod.yml`** - Production container orchestration
- **`docker-entrypoint.sh`** - Container startup script

### Quality Assurance
- **`ruff.toml`** - Modern Python linter and formatter configuration
- **`ty`** - Static type checking configuration
- **`tests/`** - Comprehensive test suite with coverage

## Prerequisites

- Docker
- [just](https://github.com/casey/just) task runner
- [uv](https://docs.astral.sh/uv/) Python Package manager

## Quick Start

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### 2. Start Development
```bash
just install  # Install dependencies
just dev      # Start app + database (http://localhost:8098)
```

### 3. Verify Everything Works
```bash
just test     # Run test suite
just req      # Test API endpoint
just browser  # Open in browser
```

## Available Commands

### Development Workflow
| Command | Description |
|---------|-------------|
| `just install` | Install dependencies using uv |
| `just dev` | Start development server + PostgreSQL |
| `just req [path]` | Send HTTP request to running server |
| `just browser` | Open development server in browser |

### Quality Assurance  
| Command | Description |
|---------|-------------|
| `just test` | Run test suite with pytest |
| `just cov` | Run tests with coverage reporting |
| `just lint` | Run ruff linter and formatter |
| `just typing` | Run mypy type checking |
| `just check-all` | Run all quality checks (lint + coverage + typing) |

### Production & Deployment
| Command | Description |
|---------|-------------|
| `just prod` | Run production server with gunicorn |
| `just prod-container` | Build and run production Docker container |
| `just build-container` | Build multi-platform Docker image |

### Lifecycle Management
| Command | Description |
|---------|-------------|
| `just update` | Update Python dependencies |
| `just fresh` | Clean install from scratch |
| `just clear` | Remove temporary files and caches |

## Configuration

Required environment variables in `.env`:

```bash
# Application settings
SERVICE_NAME=python-uv  
PORT=8098
FLASK_ENV=development

# Database connection  
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app_db
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

## Building Your Application

### 1. Add Your Routes
Start by modifying `src/python_example/app.py`:

```python
@app.route("/api/users")
def get_users():
    # Your custom logic here
    return jsonify({"users": []})
```

### 2. Create Database Models  
Add new models to `src/python_example/models.py`:

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
```

### 3. Add Dependencies
Add new packages to `pyproject.toml`:

```toml
dependencies = [
    "flask",
    "gunicorn", 
    "python-dotenv",
    "psycopg2-binary",
    "sqlalchemy",
    "your-new-package",  # Add here
]
```

Then run: `just update`

### 4. Write Tests
Add tests to `tests/test_main.py`:

```python
def test_your_endpoint(client):
    response = client.get('/api/users')
    assert response.status_code == 200
```

### 5. Configure Production
Update `compose.prod.yml` for your deployment needs:
- Environment variables
- Volume mounts  
- Resource limits
- Health checks

## API Endpoints (Demo Application)

The template includes a demo Flask app with database integration:

- **`GET /`** - System info with request logging to database
- **`GET /health`** - Health check endpoint  
- **`GET /echo/<text>`** - Echo service with text reversal

**Example response from `/`:**
```json
{
  "debug_mode": "True",
  "flask_version": "3.1.0",
  "python_version": "3.12.0 (main, ...)",
  "environment": "development",
  "service_name": "python-uv", 
  "port": "8098",
  "timestamp": "2024-01-01T12:00:00.000000",
  "recent_requests": [
    {
      "id": 1,
      "timestamp": "2024-01-01T11:59:55.123456",
      "environment": "development",
      "flask_version": "3.1.0"
    }
  ]
}
```

## Testing Strategy

```bash
just test      # Run pytest test suite
just cov       # Generate coverage report  
just typing    # Check static types
just check-all # Run all quality checks
```

**Test coverage includes:**
- All Flask endpoints (success & error cases)
- Database model operations
- Error handling and edge cases
- API response validation

## Deployment Patterns

### Local Development
```bash
just dev        # App + PostgreSQL with live reload
just req        # Test API quickly  
just check-all  # Verify code quality
```

### Production Container
```bash
just build-container     # Build optimized image
just prod-container      # Test production build locally
```

## Troubleshooting

### Environment Issues
**Missing `.env` file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

**Port conflicts:**
```bash
# Change PORT in .env file
PORT=8099 just dev
```

### Database Issues  
**PostgreSQL connection failed:**
```bash
# Restart database container
docker compose down
just dev  # Will restart PostgreSQL automatically
```

**Database schema errors:**
```bash
# Clear database and restart
docker compose down -v  # Removes volumes
just dev  # Creates fresh database
```

### Docker Issues
**Build failures:**
```bash
# Clear Docker cache
docker builder prune
just build-container
```

**Permission errors:**
```bash
# Ensure Docker daemon is running
docker ps
```

## Template Customization

### Change Application Name
1. Rename `src/python_example/` directory
2. Update imports in `app.py` and `wsgi.py`  
3. Update `SERVICE_NAME` in `.env`
4. Update `[project]` name in `pyproject.toml`

### Add New Services
Add to `compose.yml`:
```yaml
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

### Custom justfile Tasks
Add to `justfile`:
```just
# Deploy to staging
deploy-staging:
    docker build -t myapp:staging .
    docker push registry.example.com/myapp:staging
```

## Appendix A: GitHub Container Registry (ghcr.io) Configuration

To push Docker images to GitHub Container Registry (ghcr.io), you need to authenticate Docker with GitHub and configure the registry `$GIT_REGISTRY`:

### One-liner Authentication
```bash
gh auth token | docker login ghcr.io -u $(gh api user --jq .login) --password-stdin
```
### Configure `$GIT_REGISTRY`
Look at default values of [.env.example](.env.example)

### Prerequisites
- GitHub CLI (`gh`) installed and authenticated
- Docker installed and running
- Repository permissions to push packages

### Required Token Permissions
If you encounter "permission_denied" errors, ensure your GitHub token has these scopes:
- `write:packages` - Upload packages to GitHub Package Registry
- `read:packages` - Download packages from GitHub Package Registry  
- `delete:packages` - Delete packages from GitHub Package Registry (optional)
- `repo` - Full control of private repositories (if pushing to private repos)

To check/update your token permissions:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token or update existing with required scopes
3. Re-authenticate: `gh auth refresh -s write:packages,read:packages`

Once authenticated, you can use `just push-container` to push images to ghcr.io.