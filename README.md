# python-docker-uv

Flask application with Docker containerization, uv dependency management, and just for task automation.

## Prerequisites

- Docker
- [just](https://github.com/casey/just)

**That's it!** No local Python, uv, or dev tools installation required - everything runs in Docker containers.

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd python-docker-uv

# Copy environment template and configure
cp .env.example .env
```

### 2. Install Dependencies and Start Development

```bash
# Install dependencies (like npm install)
just install

# Start development server (http://localhost:8082)
just dev
```

### 3. Build for Production

```bash
# Build production image
just build

# Test production build locally
just test-prod
```

## Available Commands

| Command | Description |
|---------|-------------|
| `just install` | Install dependencies (like npm install) |
| `just dev [port]` | Start dev server with live reload (default: 8082) |
| `just test` | Run tests with pytest |
| `just check` | Run linting and type checking |
| `just format` | Format code with ruff |
| `just build [platform]` | Build Docker image (optional platform) |
| `just test-prod [port]` | Test production build locally |
| `just update` | Update Python dependencies |
| `just clean` | Remove local Docker images |

## Configuration

Required environment variables in `.env`:

```bash
SERVICE_NAME=python-docker-uv
PORT=8080
DEV_LOCAL_PORT=8082
FLASK_DEBUG=false
```

## Python Version Management

Python version is controlled by `.python-version` file:

```bash
# Check current version
cat .python-version

# Change to Python 3.11
echo "3.11" > .python-version
just build

# Change to Python 3.13
echo "3.13" > .python-version
```

## Development Workflow

```bash
just install    # Install dependencies
just dev        # Start development server with live reload
just test       # Run tests
just check      # Lint and type check
just format     # Format code
```

## API Endpoints

The Flask application provides:

- `GET /` - Returns system info and timestamp
- `GET /health` - Health check endpoint  
- `GET /echo/<text>` - Echo service for testing

Example response from `/`:
```json
{
  "message": "Hello from the cloud!",
  "python_version": "3.12.0 (main, ...)",
  "timestamp": "2024-01-01T12:00:00.000000",
  "deployed_with": "uv + Docker"
}
```

## Platform Build Strategy

| Command | Platform | Use Case |
|---------|----------|----------|
| `just build` | Host platform | Fast local development |
| `just build linux/amd64` | x86_64 | Most cloud platforms, servers |
| `just build linux/arm64` | ARM64 | ARM servers, some Macs |

## Testing

The project includes comprehensive tests:

```bash
just test           # Run all tests
just test -v        # Verbose output
just check          # Lint and type check
```

Tests cover:
- All Flask endpoints
- Error handling
- Response validation

## Troubleshooting

### Missing Environment Variables
```
error: environment variable `VARIABLE_NAME` not present
```
Solution: Ensure `.env` file exists with all required variables

### Port Already in Use
```bash
just dev 8083  # Use alternative port
```

## CI/CD

GitHub Actions workflow includes:
- Multi-version Python testing (3.9, 3.11, 3.12)
- Docker build verification
- Flask application health checks
- Linting and type checking

## License

MIT