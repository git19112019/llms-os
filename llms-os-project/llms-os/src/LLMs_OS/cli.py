"""CLI interface for LLMs_OS"""
import sys
import argparse
import logging
from pathlib import Path
from .core import execute_yaml
from .registry import list_actions
from . import __version__

def setup_logging(level: str = "INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='LLMs_OS - Workflow Automation with LLMs',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('workflow', nargs='?', help='Path to YAML workflow file')
    parser.add_argument('--version', action='version', version=f'LLMs_OS {__version__}')
    parser.add_argument('--list-actions', action='store_true', help='List available actions')
    parser.add_argument('--log-level', default='INFO', help='Logging level')
    parser.add_argument('--dev', action='store_true', help='Development mode')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # List actions
    if args.list_actions:
        print("Available actions:")
        for action in sorted(list_actions()):
            print(f"  - {action}")
        return 0
    
    # Execute workflow
    if not args.workflow:
        parser.print_help()
        return 1
    
    workflow_path = Path(args.workflow)
    if not workflow_path.exists():
        logger.error(f"Workflow file not found: {workflow_path}")
        return 1
    
    try:
        logger.info(f"Executing workflow: {workflow_path}")
        context = execute_yaml(str(workflow_path))
        logger.info("Workflow completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
