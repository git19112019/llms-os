"""Print message action"""
from typing import Dict, Any
from LLMs_OS.registry import register
from LLMs_OS.core import render

@register('print_message')
def print_message_action(task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Print a formatted message"""
    message = render(task.get('message', ''), context)
    style = task.get('style', 'info')
    
    # Color codes
    colors = {
        'info': '\033[94m',
        'success': '\033[92m',
        'warning': '\033[93m',
        'error': '\033[91m',
        'debug': '\033[90m',
    }
    reset = '\033[0m'
    
    color = colors.get(style, colors['info'])
    print(f"{color}{message}{reset}")
    
    return {'last_message': message}
