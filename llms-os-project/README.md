# LLMs OS Docker Project - Enhanced Edition

🚀 Production-ready workflow automation system with integrated Mock API, monitoring, and testing capabilities.

## Features

- ✅ **Docker-based deployment** - Multi-stage builds for minimal image sizes
- 🔌 **Mock OpenRouter API** - Test without real API keys
- 📊 **Built-in monitoring** - Prometheus + Grafana integration
- ⚡ **Async execution** - Parallel task processing
- 🔍 **Plugin system** - Extensible architecture
- 🧪 **Comprehensive testing** - Unit and integration tests
- 🔒 **Security hardened** - Non-root containers, health checks

## Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Build Docker images
make build

# Start all services
make up
```

### 2. Run Test Workflow

```bash
# Run basic test
docker-compose run --rm llms-os workflows/test_basic.yaml

# Run advanced test with parallel execution
docker-compose run --rm llms-os workflows/test_advanced.yaml
```

### 3. Access Services

- **Mock API**: http://localhost:8000
- **API Health**: http://localhost:8000/health
- **API Metrics**: http://localhost:8000/metrics

## Project Structure

```
llms-os-project/
├── docker-compose.yml              # Main services
├── docker-compose.dev.yml          # Development environment
├── docker-compose.monitoring.yml   # Monitoring stack
├── Makefile                        # Build automation
├── .env.example                    # Environment template
│
├── llms-os/                        # Main application
│   ├── Dockerfile                  # Production image
│   ├── Dockerfile.dev              # Development image
│   ├── requirements.txt            # Python dependencies
│   └── src/
│       ├── LLMs_OS/
│       │   ├── __init__.py
│       │   ├── registry.py         # Action registry
│       │   ├── core.py             # Sync execution
│       │   ├── async_core.py       # Async execution
│       │   ├── cli.py              # CLI interface
│       │   ├── exceptions.py       # Custom exceptions
│       │   ├── validators.py       # Input validation
│       │   ├── monitoring.py       # Metrics collection
│       │   ├── plugins.py          # Plugin system
│       │   └── actions/
│       │       ├── print_message.py
│       │       ├── chat_completion.py
│       │       ├── http_request.py
│       │       └── file_operations.py
│       └── tests/                  # Test suite
│
├── mock-api/                       # Mock OpenRouter API
│   ├── Dockerfile
│   └── app.py
│
├── monitoring/                     # Monitoring configs
│   ├── prometheus.yml
│   └── grafana/
│
└── workflows/                      # Example workflows
    ├── test_basic.yaml
    └── test_advanced.yaml
```

## Available Make Commands

```bash
make help         # Show all commands
make build        # Build Docker images
make up           # Start all services
make down         # Stop all services
make dev          # Start development environment
make test         # Run tests
make monitoring   # Start monitoring stack (Prometheus + Grafana)
make logs         # Show logs
make shell        # Open shell in container
make clean        # Clean up everything
```

## Available Actions

The following actions are built-in and ready to use:

- **print_message** - Display formatted messages
- **chat_completion** - Call LLM APIs (OpenRouter compatible)
- **http_request** - Make HTTP requests
- **file_read** - Read file content
- **file_write** - Write content to files

## Example Workflow

```yaml
metadata:
  title: "My Workflow"
  version: "1.0.0"

tasks:
  - action: print_message
    message: "🚀 Starting workflow..."
    style: info
  
  - action: http_request
    url: "http://mock-api:8000/health"
    method: GET
    save_as: health_check
  
  - action: chat_completion
    model: "openai/gpt-3.5-turbo"
    messages:
      - role: user
        content: "Write a haiku about Docker"
    save_as: haiku
  
  - action: print_message
    message: "AI Response: {{ haiku.content }}"
    style: success
```

## Monitoring

Start the monitoring stack:

```bash
make monitoring
```

Access dashboards:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## Development Mode

Start development environment with hot-reload:

```bash
make dev
```

Code changes are automatically reloaded without rebuilding images.

## Testing

Run the test suite:

```bash
make test
```

## Configuration

Environment variables (`.env` file):

```bash
# API Configuration
OPENROUTER_API_URL=http://mock-api:8000/api/v1
OPENROUTER_API_KEY=sk-simulated-key
MOCK_API_KEY=sk-simulated-key

# Logging
LOG_LEVEL=INFO

# Monitoring
ENABLE_METRICS=true
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

## Docker Image Sizes

- **llms-os**: ~168MB (Alpine-based, multi-stage build)
- **mock-api**: ~146MB (Slim-based)

## Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- 5GB disk space

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Python, Docker, and LLMs**
