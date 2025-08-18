# justfile for python-uv project

# ==================== Configuration ====================
# Load environment variables from .env file if it exists
set dotenv-load := true

# Python configuration (single source of truth: .python-version)
python_version := `cat .python-version | tr -d '\n'`
python_image := env_var_or_default("PYTHON_IMAGE", "python:" + python_version + "-slim")

# Port configuration
port := env_var_or_default("PORT", "8080")
dev_local_port := env_var_or_default("DEV_LOCAL_PORT", "8082")

# Local image naming
SERVICE_NAME := env_var_or_default("SERVICE_NAME", "python-uv-app")
git_hash := `git rev-parse --short HEAD`
image_tag := SERVICE_NAME + ":" + git_hash

# ==================== Default Target ====================
# Show available commands
default:
    @just --list --unsorted

# ==================== Development Commands ====================
# Start development server with Docker Compose watch mode
dev port=dev_local_port:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "🚀 Starting development server on http://localhost:{{port}}"
    echo "💡 Code changes will sync automatically with watch mode"
    echo "🛑 Press Ctrl+C to stop"
    DEV_LOCAL_PORT={{port}} docker compose up --watch


# Test production build locally
test-prod local_port=dev_local_port:
    #!/usr/bin/env bash
    set -euo pipefail
    trap 'docker stop $(docker ps -q --filter ancestor={{SERVICE_NAME}}) 2>/dev/null' EXIT
    echo "🚀 Starting production container on http://localhost:{{local_port}}"
    echo "⚠️  Note: Code changes require rebuilding the container"
    docker run -p {{local_port}}:{{port}} -e PORT={{port}} --rm {{SERVICE_NAME}}

# ==================== Build Commands ====================
# Build Docker image (defaults to host platform for speed)
build platform="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "{{platform}}" ]; then
        echo "🔨 Building Docker image for host platform..."
        docker build --build-arg PYTHON_IMAGE={{python_image}} -t {{SERVICE_NAME}} -t {{image_tag}} .
    else
        echo "🔨 Building Docker image for platform {{platform}}..."
        docker build --platform {{platform}} --build-arg PYTHON_IMAGE={{python_image}} -t {{SERVICE_NAME}} -t {{image_tag}} .
    fi

# Update dependencies
update:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📦 Updating dependencies with dockerized uv..."
    docker run --rm -v $(pwd):/app -w /app {{python_image}} sh -c "pip install uv && uv lock --upgrade"
    echo "✅ Dependencies updated in uv.lock"

# Clean up local Docker images
clean:
    #!/usr/bin/env bash
    set -euo pipefail
    docker image rm {{SERVICE_NAME}} {{image_tag}} 2>/dev/null || true
    docker image prune -f
    echo "🧹 Local Docker images cleaned"

