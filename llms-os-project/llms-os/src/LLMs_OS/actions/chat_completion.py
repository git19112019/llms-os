"""Chat completion action"""
import os
import requests
from ..registry import register

@register('chat_completion')
def chat_completion(task, context):
    """Call LLM API for chat completion"""
    api_url = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1')
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    
    model = task.get('model', 'openai/gpt-3.5-turbo')
    messages = task.get('messages', [])
    
    url = f"{api_url}/chat/completions"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'messages': messages
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        return {'content': content, 'full_response': result}
    except Exception as e:
        print(f"⚠️  Chat completion failed: {e}")
        return None
