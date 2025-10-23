"""File operations actions"""
from ..registry import register

@register('file_read')
def file_read_action(task: dict, context: dict) -> dict:
    """Read file content"""
    path = task.get('path', '')
    
    try:
        with open(path, 'r') as f:
            content = f.read()
        return {'path': path, 'content': content}
    except Exception as e:
        raise Exception(f"Failed to read file {path}: {e}")

@register('file_write')
def file_write_action(task: dict, context: dict) -> dict:
    """Write content to file"""
    path = task.get('path', '')
    content = task.get('content', '')
    mode = task.get('mode', 'w')
    
    try:
        with open(path, mode) as f:
            f.write(content)
        return {'path': path, 'bytes_written': len(content)}
    except Exception as e:
        raise Exception(f"Failed to write file {path}: {e}")
