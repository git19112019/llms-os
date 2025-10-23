"""Core workflow execution engine"""
import yaml
import os
import logging
from typing import Dict, Any
from .registry import get_action
from .exceptions import WorkflowExecutionError, ActionNotFoundError

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

def execute_yaml(yaml_path: str) -> Dict[str, Any]:
    """Execute a workflow from YAML file"""
    logger.info(f"Loading workflow from {yaml_path}")
    
    with open(yaml_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    context = {}
    metadata = workflow.get('metadata', {})
    logger.info(f"Executing workflow: {metadata.get('title', 'Untitled')}")
    
    tasks = workflow.get('tasks', [])
    for i, task in enumerate(tasks, 1):
        action_name = task.get('action')
        if not action_name:
            raise WorkflowExecutionError(f"Task {i}: Missing 'action' field")
        
        logger.info(f"Task {i}/{len(tasks)}: {action_name}")
        
        action_func = get_action(action_name)
        if not action_func:
            raise ActionNotFoundError(f"Action '{action_name}' not found")
        
        # Execute action
        result = action_func(task, context)
        
        # Save result if specified
        if 'save_as' in task:
            context[task['save_as']] = result
    
    logger.info("Workflow completed successfully")
    return context
