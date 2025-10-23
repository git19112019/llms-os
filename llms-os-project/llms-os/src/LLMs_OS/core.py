"""Core workflow execution engine"""
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
