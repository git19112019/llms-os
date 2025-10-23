"""File operations action"""
from pathlib import Path
from typing import Dict, Any
from LLMs_OS.registry import register
from LLMs_OS.core import render

@register('file_read')
def file_read_action(task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Read file content"""
    file_path = render(task.get('path', ''), context)
    encoding = task.get('encoding', 'utf-8')
    
    content = Path(file_path).read_text(encoding=encoding)
    return {'content': content, 'path': file_path}

@register('file_write')
def file_write_action(task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Write content to file"""
    file_path = render(task.get('path', ''), context)
    content = render(task.get('content', ''), context)
    encoding = task.get('encoding', 'utf-8')
    
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    Path(file_path).write_text(content, encoding=encoding)
    
    return {'path': file_path, 'bytes_written': len(content)}
