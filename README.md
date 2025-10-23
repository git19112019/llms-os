# LLMs OS Docker Project

🚀 **Production-ready workflow automation system powered by LLMs**

A Docker-based project for creating and executing automated workflows using Large Language Models. Built with Python, Docker, and includes a Mock API for testing without real API keys.

## ✨ Features

- 🐳 **Docker-based** - Containerized for easy deployment
- 🧪 **Mock API** - Test without real API keys using built-in OpenRouter simulator
- ⚡ **5 Built-in Actions** - Print, Chat, HTTP, File Read/Write
- 📊 **Monitoring Ready** - Prometheus metrics support
- 🔒 **Production Ready** - Multi-stage builds, security hardening, health checks
- 🎯 **Easy to Use** - YAML-based workflow definition
- 🔌 **Extensible** - Plugin system for custom actions

## 🚀 Quick Start

### 1. Build the Project

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/llms-os.git
cd llms-os

# Build the complete project from YAML configuration
python3 build_project.py
```

This generates the complete project in `llms-os-project/` directory.

### 2. Run Your First Workflow

```bash
# Navigate to generated project
cd llms-os-project

# Start Mock API server
docker-compose up -d mock-api

# Wait for it to be ready
sleep 3

# Run a test workflow using the convenience script
./run-workflow.sh

# Or run manually
docker run --rm \
  --network llms-os-project_llms-network \
  -e OPENROUTER_API_URL=http://llms-mock-api:8000/api/v1 \
  -e OPENROUTER_API_KEY=sk-simulated-key \
  -v $(pwd)/workflows:/app/workflows \
  llms-os:latest workflows/test_basic.yaml
```

### 3. See It Work

You should see output like:

```
🚀 Starting basic test workflow...
Environment: INFO
Health check status: 200
AI Response: I'm a mock AI assistant helping you test your workflow.
✅ Basic test completed successfully!
```

## 📚 Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup guide
- **llms-os-project/README.md** - Full project documentation (generated)
- **llms-os-project/USAGE.md** - Quick reference guide (generated)

## 🏗️ Project Architecture

```
llms-os/                                    # This repository
├── build_project.py                        # Build script
├── llms-os-docker-project-enhanced.yaml    # Source configuration
├── GETTING_STARTED.md                      # Setup guide
└── llms-os-project/                        # Generated project
    ├── docker-compose.yml                  # Service orchestration
    ├── Makefile                            # Build automation
    ├── run-workflow.sh                     # Quick run script
    ├── llms-os/                            # Main application
    │   ├── Dockerfile                      # Production image (Alpine, 168MB)
    │   ├── requirements.txt
    │   └── src/LLMs_OS/
    │       ├── core.py                     # Workflow engine
    │       ├── cli.py                      # CLI interface
    │       ├── registry.py                 # Action registry
    │       └── actions/                    # Built-in actions
    ├── mock-api/                           # Mock OpenRouter API
    │   ├── Dockerfile                      # API image (146MB)
    │   └── app.py                          # Flask-based mock server
    └── workflows/                          # Your YAML workflows
        ├── test_basic.yaml
        └── test_advanced.yaml
```

## 🎯 Available Actions

| Action | Description | Example |
|--------|-------------|---------|
| `print_message` | Display formatted messages | `message: "Hello!" style: success` |
| `chat_completion` | Call LLM API (OpenRouter compatible) | `model: "gpt-3.5-turbo"` |
| `http_request` | Make HTTP requests | `url: "..." method: GET` |
| `file_read` | Read file content | `path: "data.txt"` |
| `file_write` | Write to files | `path: "output.txt"` |

## 📝 Example Workflow

Create `workflows/my_workflow.yaml`:

```yaml
metadata:
  title: "My First Workflow"
  version: "1.0.0"

tasks:
  - action: print_message
    message: "🎉 Starting my workflow!"
    style: success
  
  - action: http_request
    url: "http://llms-mock-api:8000/api/v1/models"
    method: GET
    save_as: models
  
  - action: chat_completion
    model: "openai/gpt-3.5-turbo"
    messages:
      - role: user
        content: "Write a haiku about Docker"
    save_as: poem
  
  - action: print_message
    message: "{{ poem.content }}"
    style: success
```

Run it:
```bash
./run-workflow.sh workflows/my_workflow.yaml
```

## 🔧 Requirements

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.10+ (for build script)
- 2GB RAM minimum
- 5GB disk space

## 📦 Docker Images

After building, you'll have:

- **llms-os:latest** (168MB) - Alpine-based, multi-stage build
- **llms-os-mock-api:latest** (146MB) - Flask-based mock API

## 🛠️ Development

### Building from Source

```bash
# Build the project structure
python3 build_project.py

# Navigate to project
cd llms-os-project

# Build Docker images
docker-compose build

# Start services
docker-compose up -d
```

### Running Tests

```bash
cd llms-os-project

# Run test suite
docker-compose run --rm llms-os pytest /app/tests/ -v

# Run specific workflow
./run-workflow.sh workflows/test_basic.yaml
```

### Adding Custom Actions

1. Create new action in `llms-os-project/llms-os/src/LLMs_OS/actions/`
2. Register with `@register('action_name')` decorator
3. Rebuild Docker image: `docker-compose build llms-os`

## 🌐 Using with Real APIs

### OpenRouter API

```bash
# Get API key from https://openrouter.ai/

docker run --rm \
  -e OPENROUTER_API_URL=https://openrouter.ai/api/v1 \
  -e OPENROUTER_API_KEY=your-actual-api-key \
  -v $(pwd)/workflows:/app/workflows \
  llms-os:latest workflows/your_workflow.yaml
```

## 📊 Monitoring (Optional)

Start Prometheus + Grafana monitoring:

```bash
cd llms-os-project
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Access dashboards:
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## 🐛 Troubleshooting

### Mock API won't start

```bash
cd llms-os-project
docker-compose down
docker-compose build mock-api
docker-compose up -d mock-api
```

### Workflow action not found

Rebuild the image:
```bash
docker-compose build llms-os
```

### Port conflicts

Edit `docker-compose.yml` and change port mappings.

## 📖 Additional Resources

- **Configuration**: `llms-os-docker-project-enhanced.yaml` - Source of truth
- **Build Script**: `build_project.py` - Generates project from YAML
- **Examples**: `llms-os-project/workflows/` - Sample workflows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Support

- **Documentation**: See GETTING_STARTED.md
- **Issues**: Open an issue on GitHub
- **Discussions**: GitHub Discussions

## 🎯 Use Cases

- API testing and automation
- LLM workflow orchestration
- Data processing pipelines
- Content generation automation
- DevOps task automation
- Custom AI-powered tools

## 🔮 Future Enhancements

- [ ] Kubernetes deployment configs
- [ ] More built-in actions
- [ ] Web UI for workflow management
- [ ] Workflow scheduling
- [ ] Result persistence layer
- [ ] Authentication & authorization

---

**Built with ❤️ using Python, Docker, and LLMs**

**Star ⭐ this repo if you find it useful!**
