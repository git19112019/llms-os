"""Chat completion action using OpenRouter API"""
import os
import requests
from typing import Dict, Any
from LLMs_OS.registry import register
from LLMs_OS.core import render
from LLMs_OS.exceptions import APIError

@register('chat_completion')
def chat_completion_action(task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """Call OpenRouter API for chat completion"""
    api_url = os.getenv('OPENROUTER_API_URL', 'http://mock-api:8000/api/v1')
    api_key = os.getenv('OPENROUTER_API_KEY', 'sk-simulated-key')
    
    model = task.get('model', 'openai/gpt-3.5-turbo')
    messages = task.get('messages', [])
    
    # Render message content
    for msg in messages:
        if 'content' in msg:
            msg['content'] = render(msg['content'], context)
    
    # Make API call
    response = requests.post(
        f"{api_url}/chat/completions",
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json={
            'model': model,
            'messages': messages,
            'temperature': task.get('temperature', 0.7),
            'max_tokens': task.get('max_tokens', 150)
        },
        timeout=30
    )
    
    if response.status_code != 200:
        raise APIError(f"API request failed: {response.text}", response.status_code)
    
    result = response.json()
    content = result['choices'][0]['message']['content']
    
    return {'content': content, 'response': result}
