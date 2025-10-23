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
    create_file(output_dir / 'llms-os/src/LLMs_OS/registry.py', source_files.get('registry', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/core.py', source_files.get('core', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/async_core.py', source_files.get('async_core', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/cli.py', source_files.get('cli', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/exceptions.py', source_files.get('exceptions', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/validators.py', source_files.get('validators', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/monitoring.py', source_files.get('monitoring', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/plugins.py', source_files.get('plugins', ''))
    
    # Actions
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/__init__.py', source_files.get('actions_init', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/print_message.py', source_files.get('action_print', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/chat_completion.py', source_files.get('action_chat', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/http_request.py', source_files.get('action_http', ''))
    create_file(output_dir / 'llms-os/src/LLMs_OS/actions/file_operations.py', source_files.get('action_file', ''))
    
    # Tests
    create_file(output_dir / 'llms-os/src/tests/__init__.py', '')
    create_file(output_dir / 'llms-os/src/tests/test_core.py', source_files.get('test_core', ''))
    create_file(output_dir / 'llms-os/src/tests/test_actions.py', source_files.get('test_actions', ''))
    
    # Setup.py
    create_file(output_dir / 'llms-os/src/setup.py', source_files.get('setup', ''))
    print()
    
    # Create mock API
    print('🔌 Creating Mock API...')
    api_files = config.get('mock_api', {})
    create_file(output_dir / 'mock-api/app.py', api_files.get('app', ''))
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
