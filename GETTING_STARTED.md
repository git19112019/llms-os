# 🚀 Getting Started with LLMs OS Docker Project

This guide will help you build and run the project from scratch.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.10+ (for build script)
- Git

## Quick Start (2 Steps)

### Step 1: Build the Project

```bash
# Clone the repository (if you haven't already)
git clone <your-repo-url>
cd llms-os

# Build the complete project from YAML
python3 build_project.py

# This creates the llms-os-project/ directory with all files
```

### Step 2: Run It

```bash
# Navigate to the generated project
cd llms-os-project

# Start Mock API
docker-compose up -d mock-api

# Wait a few seconds for API to be ready
sleep 3

# Run a test workflow
./run-workflow.sh
```

## What You Should See

```
🚀 Starting Mock API...
✅ Mock API started
📝 Running workflow: workflows/test_basic.yaml

2025-10-23 09:30:05 - INFO - Executing workflow: test_basic.yaml
🚀 Starting basic test workflow...
Environment: INFO
Health check status: 200
AI Response: I'm a mock AI assistant helping you test your workflow.
✅ Basic test completed successfully!
2025-10-23 09:30:06 - INFO - Workflow completed successfully

✅ Workflow completed!
```

## Project Structure After Build

```
llms-os/                        # This repository
├── build_project.py            # Build script
├── llms-os-docker-project-enhanced.yaml  # Source config
└── llms-os-project/            # Generated project (created by build script)
    ├── docker-compose.yml
    ├── Makefile
    ├── run-workflow.sh         # Quick run script
    ├── README.md               # Full documentation
    ├── USAGE.md                # Quick reference
    ├── llms-os/                # Main application
    │   ├── Dockerfile
    │   └── src/LLMs_OS/
    ├── mock-api/               # Mock OpenRouter API
    │   ├── Dockerfile
    │   └── app.py
    └── workflows/              # Your YAML workflows
        ├── test_basic.yaml
        └── test_advanced.yaml
```

## Common Commands

```bash
# Build the project
python3 build_project.py

# Navigate to project
cd llms-os-project

# Build Docker images (done automatically by build_project.py)
make build

# Start Mock API
docker-compose up -d mock-api

# Run a workflow (easiest way)
./run-workflow.sh workflows/test_basic.yaml

# Run a workflow (manual way)
docker run --rm \
  --network llms-os-project_llms-network \
  -e OPENROUTER_API_URL=http://llms-mock-api:8000/api/v1 \
  -e OPENROUTER_API_KEY=sk-simulated-key \
  -v $(pwd)/workflows:/app/workflows \
  llms-os:latest workflows/test_basic.yaml

# Check API health
curl http://localhost:8000/health

# View logs
docker logs llms-mock-api

# Stop everything
docker-compose down
```

## Creating Your Own Workflow

```bash
cd llms-os-project

# Create a new workflow
cat > workflows/my_workflow.yaml << 'YAML'
metadata:
  title: "My Custom Workflow"
  version: "1.0.0"

tasks:
  - action: print_message
    message: "🎉 Starting my workflow!"
    style: success
  
  - action: http_request
    url: "http://llms-mock-api:8000/api/v1/models"
    method: GET
    save_as: models
  
  - action: print_message
    message: "Found {{ models.json.data | length }} models"
    style: info
  
  - action: chat_completion
    model: "openai/gpt-3.5-turbo"
    messages:
      - role: user
        content: "Write a haiku about automation"
    save_as: haiku
  
  - action: print_message
    message: "{{ haiku.content }}"
    style: success
YAML

# Run it
./run-workflow.sh workflows/my_workflow.yaml
```

## Troubleshooting

### Issue: "Mock API is unhealthy"

**Solution:**
```bash
# Stop everything
docker-compose down

# Rebuild mock API
docker-compose build mock-api

# Start it
docker-compose up -d mock-api

# Wait and check
sleep 3
curl http://localhost:8000/health
```

### Issue: "Action not found"

**Solution:** The Docker image needs to be rebuilt after code changes.
```bash
docker-compose build llms-os
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find what's using port 8000
lsof -i :8000

# Stop the conflicting service or change port in docker-compose.yml
# Change "8000:8000" to "8001:8000"
```

## Using with Real API

To use with OpenRouter instead of Mock API:

```bash
# Get API key from https://openrouter.ai/

# Run workflow with real API
docker run --rm \
  -e OPENROUTER_API_URL=https://openrouter.ai/api/v1 \
  -e OPENROUTER_API_KEY=your-real-api-key \
  -v $(pwd)/workflows:/app/workflows \
  llms-os:latest workflows/test_basic.yaml
```

## Next Steps

1. ✅ Build project: `python3 build_project.py`
2. ✅ Start services: `cd llms-os-project && docker-compose up -d mock-api`
3. ✅ Test it: `./run-workflow.sh`
4. 📝 Read full docs: `cat llms-os-project/README.md`
5. 📋 Quick reference: `cat llms-os-project/USAGE.md`
6. ✨ Create custom workflows
7. 🚀 Deploy to production

## Support

- **Full Documentation**: `llms-os-project/README.md`
- **Quick Reference**: `llms-os-project/USAGE.md`
- **Source Config**: `llms-os-docker-project-enhanced.yaml`
- **Issues**: Open an issue on GitHub

---

**Happy Automating! 🎉**
