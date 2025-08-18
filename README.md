# python-uv

Flask application template for containerized deployment using Docker, uv package management, and just for task automation.

**🚀 Zero Configuration Required** - Clone and run `just dev` to get started immediately!

## Prerequisites

- Docker
- [just](https://github.com/casey/just)

**For cloud deployment (optional):**
- Cloud provider CLI tools
- [jq](https://jqlang.github.io/jq/) - For log formatting

Note: No local Python or uv installation required.

## Quick Start

### 1. Start Development (Zero Configuration)

```bash
# Clone the repository
git clone <repository-url>
cd python-uv

# Start development server immediately (http://localhost:8082)
just dev
```

**That's it!** The project uses sensible defaults and requires no configuration for local development.

### 2. Build for Production

```bash
# Build production image
just build

# Test production build locally
just test-prod
```

## Available Commands

### Development
| Command | Description |
|---------|-------------|
| `just dev [port]` | Start dev server with live reload (default: 8082) |
| `just test-prod [port]` | Test production build locally |
| `just update` | Update Python dependencies |

### Build & Maintenance
| Command | Description |
|---------|-------------|
| `just build [platform]` | Build Docker image (optional platform) |
| `just clean` | Remove local Docker images |

## Configuration (Optional)

The project works with minimal configuration using these defaults:

- **Service Name**: `python-uv-app`
- **Ports**: `8080` (production), `8082` (development)

**To customize**: Copy `.env.example` to `.env` and modify any values.

### Python Version Management

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

The system automatically:
- Derives the Docker image (`python:X.Y-slim`)
- Manages version-specific dependencies
- Ensures consistency across all environments

## Development Workflow

### Local Development

```bash
just dev
```

Uses Docker Compose with watch mode for automatic file syncing and live reload.

### Testing Production Build

```bash
just build           # Build container
just test-prod       # Run production container locally
```


## Platform Build Strategy

The project supports different platforms:

| Command | Platform | Use Case |
|---------|----------|----------|
| `just build` | Host platform | Fast local development |
| `just build linux/amd64` | x86_64 | Most cloud platforms, servers |
| `just build linux/arm64` | ARM64 | ARM servers, some Macs |

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


## CI/CD and Automated Testing

This repository includes GitHub Actions workflows for automated testing:

### 🧪 Continuous Integration

Pull requests and main branch pushes trigger:
- Multi-version Python testing (3.9, 3.11, 3.12)
- Docker build verification
- Flask application health checks

### 🏷️ Release Management

The system supports semantic versioning:
- `v1.0.0` - Major releases
- `v1.1.0` - Minor features
- `v1.1.1` - Patches and fixes

## License

MIT

## Support

For issues or questions:
- Review troubleshooting section above
- Open an issue on GitHub
