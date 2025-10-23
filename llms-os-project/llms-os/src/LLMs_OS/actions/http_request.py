"""HTTP request action"""
import requests
from ..registry import register

@register('http_request')
def http_request(task, context):
    """Make an HTTP request"""
    url = task.get('url', '')
    method = task.get('method', 'GET').upper()
    headers = task.get('headers', {})
    data = task.get('data')
    
    try:
        response = requests.request(method, url, headers=headers, json=data, timeout=30)
        return {
            'status_code': response.status_code,
            'content': response.text,
            'json': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        print(f"⚠️  HTTP request failed: {e}")
        return None
