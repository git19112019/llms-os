"""Command-line interface for LLMs OS"""
import sys
import argparse
from .core import execute_yaml

def main():
    parser = argparse.ArgumentParser(description='LLMs OS Workflow Automation')
    parser.add_argument('workflow', help='Path to workflow YAML file')
    parser.add_argument('--log-level', default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    try:
        execute_yaml(args.workflow)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
