"""HTTP request action"""
import requests
from typing import Dict, Any
from LLMs_OS.registry import register
from LLMs_OS.core import render
from LLMs_OS.exceptions import APIError

@register('http_request')
def http_request_action(task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Make HTTP request"""
    url = render(task.get('url', ''), context)
    method = task.get('method', 'GET').upper()
    headers = task.get('headers', {})
    body = task.get('body')
    timeout = task.get('timeout', 30)
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body if body else None,
            timeout=timeout
        )
        
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.text,
            'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        if not task.get('ignore_errors', False):
            raise APIError(f"HTTP request failed: {e}")
        return {'error': str(e)}
