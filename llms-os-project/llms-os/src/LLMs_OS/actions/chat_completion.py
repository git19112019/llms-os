"""Chat completion action"""
import os
import requests
from ..registry import register
from ..exceptions import APIError

@register('chat_completion')
def chat_completion_action(task: dict, context: dict) -> dict:
    """Call LLM API for chat completion"""
    api_url = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1')
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    
    model = task.get('model', 'openai/gpt-3.5-turbo')
    messages = task.get('messages', [])
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': model,
        'messages': messages
    }
    
    try:
        response = requests.post(
            f'{api_url}/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        return {'content': content, 'model': model}
        
    except requests.RequestException as e:
        raise APIError(f"API request failed: {e}")
