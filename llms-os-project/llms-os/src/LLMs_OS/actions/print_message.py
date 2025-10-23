"""Print message action"""
import re
from ..registry import register

COLORS = {
    'success': '\033[92m',
    'error': '\033[91m',
    'warning': '\033[93m',
    'info': '\033[94m',
    'debug': '\033[90m',
    'reset': '\033[0m'
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
            default_match = re.search(r"default\(['\"](.+?)['\"]\)", default_part)
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
    
    message = re.sub(r'\{\{\s*(.+?)\s*\}\}', replace_var, message)
    
    color = COLORS.get(style, COLORS['info'])
    print(f"{color}{message}{COLORS['reset']}")
    return None
