.PHONY: help build up down test clean dev monitoring logs shell

# Default target
help:
	@echo "LLMs_OS Docker Project - Available Commands:"
	@echo ""
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make dev         - Start development environment"
	@echo "  make test        - Run tests"
	@echo "  make monitoring  - Start monitoring stack"
	@echo "  make logs        - Show logs"
	@echo "  make shell       - Open shell in llms-os container"
	@echo "  make clean       - Clean up everything"
	@echo ""

# Build Docker images
build:
	@echo "🏗️ Building Docker images..."
	docker-compose build
	@echo "✅ Build complete!"

# Start services
up: build
	@echo "🚀 Starting services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo ""
	@echo "📍 Services available at:"
	@echo "  - Mock API: http://localhost:8000"
	@echo "  - API Health: http://localhost:8000/health"
	@echo "  - API Metrics: http://localhost:8000/metrics"
	@echo ""

# Stop services
down:
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✅ Services stopped!"

# Development mode
dev:
	@echo "🔧 Starting development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Run tests
test:
	@echo "🧪 Running tests..."
	docker-compose exec llms-os pytest -v /app/tests/
	@echo "✅ Tests complete!"

# Start monitoring
monitoring:
	@echo "📊 Starting monitoring stack..."
	docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
	@echo "✅ Monitoring started!"
	@echo ""
	@echo "📍 Monitoring available at:"
	@echo "  - Prometheus: http://localhost:9090"
	@echo "  - Grafana: http://localhost:3000 (admin/admin)"
	@echo ""

# Show logs
logs:
	docker-compose logs -f --tail=100

# Open shell
shell:
	docker-compose exec llms-os /bin/sh

# Clean everything
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f
	rm -rf output/* logs/*
	@echo "✅ Cleanup complete!"
