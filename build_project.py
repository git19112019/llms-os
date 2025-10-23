#!/usr/bin/env python3
"""
Build script to generate the complete LLMs OS Docker project from YAML
"""
import yaml
import sys
from pathlib import Path

def create_file(path: Path, content: str):
    """Create a file with content"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + '\n')
    print(f'  ✅ {path.relative_to(path.parents[len(path.parents)-2])}')

def main():
    yaml_file = Path('llms-os-docker-project-enhanced.yaml')
    output_dir = Path('llms-os-project')
    
    print(f'🚀 Building LLMs OS Docker Project...\n')
    
    # Load YAML config
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Create base structure
    print('📁 Creating directory structure...')
    dirs = [
        'llms-os/src/LLMs_OS/actions',
        'llms-os/src/tests',
        'mock-api',
        'monitoring/grafana/dashboards',
        'workflows/production',
        'scripts',
        'output',
        'logs'
    ]
    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)
    print('  ✅ Directories created\n')
    
    # Create Docker files
    print('🐳 Creating Docker configurations...')
    docker_config = config.get('docker', {})
    create_file(output_dir / 'llms-os/Dockerfile', docker_config.get('dockerfile_main', ''))
    create_file(output_dir / 'llms-os/Dockerfile.dev', docker_config.get('dockerfile_dev', ''))
    create_file(output_dir / 'mock-api/Dockerfile', docker_config.get('dockerfile_mock_api', ''))
    
    # Create docker-compose files
    compose_config = config.get('docker_compose', {})
    create_file(output_dir / 'docker-compose.yml', compose_config.get('main', ''))
    create_file(output_dir / 'docker-compose.dev.yml', compose_config.get('dev', ''))
    create_file(output_dir / 'docker-compose.monitoring.yml', compose_config.get('monitoring', ''))
    print()
    
    # Create config files
    print('⚙️  Creating configuration files...')
    config_files = config.get('config_files', {})
    create_file(output_dir / 'Makefile', config_files.get('makefile', ''))
    create_file(output_dir / 'llms-os/requirements.txt', config_files.get('requirements', ''))
    create_file(output_dir / 'llms-os/requirements.dev.txt', config_files.get('requirements_dev', ''))
    create_file(output_dir / '.env.example', config_files.get('env_example', ''))
    create_file(output_dir / '.dockerignore', config_files.get('dockerignore', ''))
    print()
    
    # Create source files
    print('📝 Creating source code files...')
    source_files = config.get('source_files', {})
    
    # Main LLMs_OS files
    create_file(output_dir / 'llms-os/src/LLMs_OS/__init__.py', source_files.get('llms_os_init', ''))
    
    # Registry
    registry_code = '''"""Action registry for LLMs_OS"""

_ACTIONS = {}

def register(name):
    """Decorator to register an action"""
    def decorator(func):
        _ACTIONS[name] = func
        return func
    return decorator

def get_action(name):
    """Get an action by name"""
    if name not in _ACTIONS:
        raise KeyError(f"Action not found: {name}")
    return _ACTIONS[name]

def list_actions():
    """List all registered actions"""
    return list(_ACTIONS.keys())
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/registry.py', registry_code)
    
    # Core
    core_code = '''"""Core workflow execution engine"""
import yaml
import os
from pathlib import Path
from .registry import get_action

def execute_yaml(file_path: str) -> None:
    """Execute a workflow from a YAML file"""
    # Load workflow
    with open(file_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Import actions to ensure they're registered
    import LLMs_OS.actions
    
    # Get tasks
    tasks = workflow.get('tasks', [])
    context = {}
    
    # Execute each task
    for task in tasks:
        action_name = task.get('action')
        if not action_name:
            continue
        
        try:
            action = get_action(action_name)
            result = action(task, context)
            
            # Save result if requested
            if 'save_as' in task and result:
                context[task['save_as']] = result
        except Exception as e:
            print(f"❌ Error in action '{action_name}': {e}")
            raise
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/core.py', core_code)
    
    create_file(output_dir / 'llms-os/src/LLMs_OS/async_core.py', source_files.get('async_core', ''))
    
    # CLI
    cli_code = '''"""Command-line interface for LLMs_OS"""
import sys
import argparse
from pathlib import Path
from .core import execute_yaml

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='LLMs_OS - Workflow automation with LLMs')
    parser.add_argument('workflow', nargs='?', help='Path to workflow YAML file')
    parser.add_argument('--version', action='store_true', help='Show version')
    
    args = parser.parse_args()
    
    if args.version:
        print('LLMs_OS v1.0.0')
        return 0
    
    if not args.workflow:
        parser.print_help()
        return 1
    
    workflow_path = Path(args.workflow)
    if not workflow_path.exists():
        print(f"❌ Workflow file not found: {workflow_path}")
        return 1
    
    try:
        execute_yaml(str(workflow_path))
        return 0
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/cli.py', cli_code)
    
    create_file(output_dir / 'llms-os/src/LLMs_OS/exceptions.py', source_files.get('exceptions', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/validators.py', source_files.get('validators', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/monitoring.py', source_files.get('monitoring', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/plugins.py', source_files.get('plugins', ''))
    
    # Actions init
    actions_init_code = '''"""Action modules"""
from . import print_message
from . import chat_completion
from . import http_request
from . import file_operations

__all__ = ['print_message', 'chat_completion', 'http_request', 'file_operations']
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/__init__.py', actions_init_code)
    
    # Print message action
    print_action_code = '''"""Print message action"""
import re
from ..registry import register

COLORS = {
    'success': '\\033[92m',
    'error': '\\033[91m',
    'warning': '\\033[93m',
    'info': '\\033[94m',
    'debug': '\\033[90m',
    'reset': '\\033[0m'
}

@register('print_message')
def print_message(task, context):
    """Print a formatted message"""
    message = task.get('message', '')
    style = task.get('style', 'info')
    
    # Replace templates like {{ var }} or {{ var.attr }}
    def replace_var(match):
        var_path = match.group(1).strip()
        
        # Handle default values: {{ var | default('value') }}
        if '|' in var_path:
            var_part, default_part = var_path.split('|', 1)
            var_path = var_part.strip()
            # Extract default value from default('value')
            default_match = re.search(r"default\\(['\\\"](.+?)['\\\"]\\)", default_part)
            default_val = default_match.group(1) if default_match else ''
        else:
            default_val = ''
        
        # Navigate path (e.g., health_check.status_code)
        parts = var_path.split('.')
        value = context
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
                if value is None:
                    return default_val if default_val else match.group(0)
            else:
                return default_val if default_val else match.group(0)
        
        return str(value) if value is not None else default_val
    
    message = re.sub(r'\\{\\{\\s*(.+?)\\s*\\}\\}', replace_var, message)
    
    color = COLORS.get(style, COLORS['info'])
    print(f"{color}{message}{COLORS['reset']}")
    return None
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/print_message.py', print_action_code)
    
    # Chat completion action
    chat_action_code = '''"""Chat completion action"""
import os
import requests
from ..registry import register

@register('chat_completion')
def chat_completion(task, context):
    """Call LLM API for chat completion"""
    api_url = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1')
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    
    model = task.get('model', 'openai/gpt-3.5-turbo')
    messages = task.get('messages', [])
    
    url = f"{api_url}/chat/completions"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'messages': messages
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        return {'content': content, 'full_response': result}
    except Exception as e:
        print(f"⚠️  Chat completion failed: {e}")
        return None
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/chat_completion.py', chat_action_code)
    
    # HTTP request action
    http_action_code = '''"""HTTP request action"""
import requests
from ..registry import register

@register('http_request')
def http_request(task, context):
    """Make an HTTP request"""
    url = task.get('url', '')
    method = task.get('method', 'GET').upper()
    headers = task.get('headers', {})
    data = task.get('data')
    
    try:
        response = requests.request(method, url, headers=headers, json=data, timeout=30)
        return {
            'status_code': response.status_code,
            'content': response.text,
            'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        print(f"⚠️  HTTP request failed: {e}")
        return None
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/http_request.py', http_action_code)
    
    # File operations action
    file_action_code = '''"""File operations actions"""
from pathlib import Path
from ..registry import register

@register('file_read')
def file_read(task, context):
    """Read file content"""
    path = task.get('path', '')
    try:
        with open(path, 'r') as f:
            content = f.read()
        return {'content': content}
    except Exception as e:
        print(f"⚠️  File read failed: {e}")
        return None

@register('file_write')
def file_write(task, context):
    """Write content to file"""
    path = task.get('path', '')
    content = task.get('content', '')
    
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return {'path': path}
    except Exception as e:
        print(f"⚠️  File write failed: {e}")
        return None
'''
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/file_operations.py', file_action_code)
    
    # Tests
    create_file(output_dir / 'llms-os/src/tests/__init__.py', '')
    create_file(output_dir / 'llms-os/src/tests/test_core.py', source_files.get('test_core', ''))
    create_file(output_dir / 'llms-os/src/tests/test_actions.py', source_files.get('test_actions', ''))
    
    # pyproject.toml for modern Python packaging
    pyproject_content = '''[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "LLMs_OS"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = []

[project.scripts]
llms-os = "LLMs_OS.cli:main"

[tool.setuptools]
packages = ["LLMs_OS", "LLMs_OS.actions"]
'''
    create_file(output_dir / 'llms-os/src/pyproject.toml', pyproject_content)
    print()
    
    # Create mock API
    print('🔌 Creating Mock API...')
    mock_api_app = source_files.get('mock_api_app', '')
    create_file(output_dir / 'mock-api/app.py', mock_api_app)
    print()
    
    # Create monitoring configs
    print('📊 Creating monitoring configurations...')
    monitoring_config = config.get('monitoring_config', {})
    create_file(output_dir / 'monitoring/prometheus.yml', monitoring_config.get('prometheus', ''))
    create_file(output_dir / 'monitoring/grafana/dashboards/llms-os.json', monitoring_config.get('grafana_dashboard', '{}'))
    print()
    
    # Create workflows
    print('🔄 Creating test workflows...')
    workflows = config.get('test_workflows', {})
    create_file(output_dir / 'workflows/test_basic.yaml', workflows.get('test_basic', ''))
    create_file(output_dir / 'workflows/test_advanced.yaml', workflows.get('test_advanced', ''))
    print()
    
    # Create README
    print('📖 Creating documentation...')
    create_file(output_dir / 'README.md', config.get('readme', {}).get('content', '# LLMs OS Docker Project'))
    print()
    
    print('✅ Project build complete!')
    print(f'\n📦 Project created at: {output_dir.absolute()}')
    print('\n🚀 Quick start:')
    print(f'  cd {output_dir}')
    print('  cp .env.example .env')
    print('  make build')
    print('  make up')

if __name__ == '__main__':
    main()
