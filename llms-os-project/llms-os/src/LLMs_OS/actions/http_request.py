"""HTTP request action"""
import requests
from ..registry import register
from ..exceptions import APIError

@register('http_request')
def http_request_action(task: dict, context: dict) -> dict:
    """Make HTTP requests"""
    url = task.get('url', '')
    method = task.get('method', 'GET').upper()
    headers = task.get('headers', {})
    data = task.get('data')
    
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            json=data if method in ['POST', 'PUT', 'PATCH'] else None,
            timeout=30
        )
        response.raise_for_status()
        
        return {
            'status_code': response.status_code,
            'data': response.json() if response.content else None,
            'headers': dict(response.headers)
        }
        
    except requests.RequestException as e:
        raise APIError(f"HTTP request failed: {e}")
