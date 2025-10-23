"""Print message action"""
from ..registry import register

STYLES = {
    'success': '\033[92m',  # Green
    'error': '\033[91m',    # Red
    'warning': '\033[93m',  # Yellow
    'info': '\033[94m',     # Blue
    'reset': '\033[0m'
}

@register('print_message')
def print_message_action(task: dict, context: dict) -> dict:
    """Print a message with optional styling"""
    message = task.get('message', '')
    style = task.get('style', 'info')
    
    # Simple template replacement
    import re
    for key, value in context.items():
        # Handle nested attributes like {{ key.attribute }}
        if isinstance(value, dict):
            for attr, attr_value in value.items():
                pattern = f'{{{{ *{key}\\.{attr} *}}}}'
                message = re.sub(pattern, str(attr_value), message)
        # Handle simple variables like {{ key }}
        pattern = f'{{{{ *{key} *}}}}'
        message = re.sub(pattern, str(value), message)
    
    color = STYLES.get(style, STYLES['info'])
    reset = STYLES['reset']
    print(f"{color}{message}{reset}")
    
    return {'message': message, 'style': style}
