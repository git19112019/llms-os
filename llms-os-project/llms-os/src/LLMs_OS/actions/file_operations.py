"""File operations actions"""
from pathlib import Path
from ..registry import register

@register('file_read')
def file_read(task, context):
    """Read file content"""
    path = task.get('path', '')
    try:
        with open(path, 'r') as f:
            content = f.read()
        return {'content': content}
    except Exception as e:
        print(f"⚠️  File read failed: {e}")
        return None

@register('file_write')
def file_write(task, context):
    """Write content to file"""
    path = task.get('path', '')
    content = task.get('content', '')
    
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return {'path': path}
    except Exception as e:
        print(f"⚠️  File write failed: {e}")
        return None
