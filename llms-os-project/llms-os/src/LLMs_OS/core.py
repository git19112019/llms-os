"""Core execution engine for LLMs_OS"""
import yaml
import os
from typing import Dict, Any
from jinja2 import Template
from .registry import get_action
from .exceptions import WorkflowExecutionError, ActionNotFoundError
from .validators import WorkflowValidator
from .monitoring import MetricsCollector, active_workflows

def render(template_str: str, context: Dict[str, Any]) -> str:
    """Render Jinja2 template with context"""
    if not isinstance(template_str, str):
        return template_str
    try:
        template = Template(template_str)
        return template.render(context)
    except Exception as e:
        return template_str

def execute_yaml(file_path: str) -> Dict[str, Any]:
    """Execute workflow from YAML file"""
    # Load workflow
    with open(file_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)
    
    # Validate
    WorkflowValidator.validate(workflow)
    
    # Execute with tracking
    with MetricsCollector.track_workflow():
        context = {
            'env': dict(os.environ),
            'workflow': workflow.get('metadata', {})
        }
        
        tasks = workflow.get('tasks', [])
        for task in tasks:
            action_name = task.get('action')
            action_func = get_action(action_name)
            
            if not action_func:
                raise ActionNotFoundError(f"Action not found: {action_name}")
            
            # Execute action
            try:
                result = action_func(task, context)
                if result and isinstance(result, dict):
                    context.update(result)
                    
                # Save result if needed
                save_as = task.get('save_as')
                if save_as and result:
                    context[save_as] = result
                    
            except Exception as e:
                if not task.get('ignore_errors', False):
                    raise WorkflowExecutionError(f"Task failed: {e}") from e
        
        return context
