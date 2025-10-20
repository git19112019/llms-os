# LLMs_OS Docker Project Enhanced

This is a production-ready LLMs_OS with Mock API, Monitoring & Testing capabilities.

## Features
- Mock OpenRouter API for testing
- Async task execution
- Plugin system
- Monitoring with Prometheus/Grafana
- Comprehensive testing
- Security hardening

## Directory Structure
```
project/
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.monitoring.yml
├── Makefile
├── .env.example
├── README.md
├── llms-os/                    # Main CLI Application
├── mock-api/                    # Mock OpenRouter API
├── monitoring/                  # Monitoring configs
├── workflows/                   # Workflow examples
└── scripts/                     # Utility scripts
```

## Quick Start
Follow these steps to get the project up and running:

1.  **Navigate to the project directory:**
    ```bash
    cd my-llms-os-project
    ```

2.  **Copy environment file:**
    ```bash
    cp .env.example .env
    ```

3.  **Build all Docker images:**
    ```bash
    make build
    ```

4.  **Start all services:**
    ```bash
    make up
    ```
    Services will be available at:
    -   Mock API: `http://localhost:8000`
    -   API Health: `http://localhost:8000/health`
    -   API Metrics: `http://localhost:8000/metrics`

5.  **Run tests:**
    ```bash
    make test
    ```

## Monitoring
To start the monitoring stack (Prometheus and Grafana):

```bash
make monitoring
```
Monitoring will be available at:
-   Prometheus: `http://localhost:9090`
-   Grafana: `http://localhost:3000` (admin/admin)

## Development
To start the development environment with hot reload:

```bash
make dev
```

## License
This project is licensed under the MIT License.
