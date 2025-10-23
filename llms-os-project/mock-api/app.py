"""Mock OpenRouter API for testing"""
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'mock-api'}), 200

@app.route('/api/v1/models', methods=['GET'])
def list_models():
    return jsonify({
        'data': [
            {'id': 'openai/gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo'},
            {'id': 'openai/gpt-4', 'name': 'GPT-4'},
        ]
    })

@app.route('/api/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    model = data.get('model', 'openai/gpt-3.5-turbo')
    messages = data.get('messages', [])
    
    # Mock response
    response = {
        'id': 'mock-123',
        'object': 'chat.completion',
        'created': 1234567890,
        'model': model,
        'choices': [{
            'index': 0,
            'message': {
                'role': 'assistant',
                'content': "This is a mock response from the LLMs Mock API. I'm simulating an AI assistant for testing purposes."
            },
            'finish_reason': 'stop'
        }],
        'usage': {
            'prompt_tokens': 10,
            'completion_tokens': 20,
            'total_tokens': 30
        }
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    print("🚀 Starting Mock API on port 8000...")
    app.run(host='0.0.0.0', port=8000, debug=True)
