# LLMs OS Docker Project - Quick Usage Guide

## 🚀 Quick Start (3 Simple Steps)

### 1. Start the Mock API
```bash
cd /workspaces/llms-os/llms-os-project
docker-compose up -d mock-api
```

### 2. Run a Workflow
```bash
# Using the convenience script
./run-workflow.sh

# Or manually
docker run --rm \
  --network llms-os-project_llms-network \
  -e OPENROUTER_API_URL=http://llms-mock-api:8000/api/v1 \
  -e OPENROUTER_API_KEY=sk-simulated-key \
  -v $(pwd)/workflows:/app/workflows \
  llms-os:latest workflows/test_basic.yaml
```

### 3. Create Your Own Workflow
```bash
# Copy example
cp workflows/test_basic.yaml workflows/my_workflow.yaml

# Edit it
nano workflows/my_workflow.yaml

# Run it
./run-workflow.sh workflows/my_workflow.yaml
```

## 📚 Available Actions

| Action | Description | Example |
|--------|-------------|---------|
| `print_message` | Display formatted text | `message: "Hello!" style: success` |
| `chat_completion` | Call LLM API | `model: "gpt-3.5-turbo" messages: [...]` |
| `http_request` | Make HTTP calls | `url: "..." method: GET` |
| `file_read` | Read files | `path: "data.txt"` |
| `file_write` | Write files | `path: "output.txt" content: "..."` |

## 📖 Workflow Structure

```yaml
metadata:
  title: "My Workflow"
  version: "1.0.0"

tasks:
  - action: print_message
    message: "Starting..."
    style: info
  
  - action: http_request
    url: "http://api.example.com/data"
    save_as: api_result
  
  - action: print_message
    message: "Got {{ api_result.status_code }} response"
```

## 🛠️ Useful Commands

```bash
# Check API health
curl http://localhost:8000/health

# List available models
curl http://localhost:8000/api/v1/models

# View logs
docker logs llms-mock-api

# List actions
docker run --rm llms-os:latest --list-actions

# Stop everything
docker-compose down
```

## 🎯 Common Use Cases

### 1. API Testing
```yaml
tasks:
  - action: http_request
    url: "http://llms-mock-api:8000/api/v1/models"
    save_as: result
  - action: print_message
    message: "Status: {{ result.status_code }}"
```

### 2. LLM Automation
```yaml
tasks:
  - action: chat_completion
    model: "openai/gpt-3.5-turbo"
    messages:
      - role: user
        content: "Generate a todo list"
    save_as: todos
  - action: file_write
    path: "todos.txt"
    content: "{{ todos.content }}"
```

### 3. Data Processing Pipeline
```yaml
tasks:
  - action: file_read
    path: "input.txt"
    save_as: data
  - action: chat_completion
    messages:
      - role: user
        content: "Summarize: {{ data.content }}"
    save_as: summary
  - action: file_write
    path: "summary.txt"
    content: "{{ summary.content }}"
```

## 💡 Tips

1. **Use variables**: `{{ variable_name }}` for Jinja2 templating
2. **Save results**: `save_as: result_name` to use in later steps
3. **Error handling**: Add `ignore_errors: true` to continue on failure
4. **Environment vars**: Access with `{{ env.VAR_NAME }}`

## 🔗 Resources

- Project directory: `/workspaces/llms-os/llms-os-project`
- Example workflows: `workflows/`
- Full README: `README.md`
- Mock API docs: http://localhost:8000

---
**Need help?** Check the README.md for detailed documentation.
