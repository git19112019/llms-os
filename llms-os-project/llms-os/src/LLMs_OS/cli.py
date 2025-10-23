"""Command-line interface for LLMs_OS"""
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
