"""Mock OpenRouter API for testing"""
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import random
import hashlib
import json

app = Flask(__name__)
CORS(app)

SIMULATED_API_KEY = "sk-simulated-key"
ENABLE_METRICS = True

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": int(time.time())}), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    """Metrics endpoint"""
    return "# Mock metrics\napi_requests_total 0\n", 200

@app.route("/api/v1/models", methods=["GET"])
def list_models():
    """List available models"""
    models = [
        {"id": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo"},
        {"id": "openai/gpt-4", "name": "GPT-4"},
        {"id": "anthropic/claude-2", "name": "Claude 2"},
    ]
    return jsonify({"data": models}), 200

@app.route("/api/v1/chat/completions", methods=["POST"])
def chat_completions():
    """Mock chat completions endpoint"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith(f"Bearer {SIMULATED_API_KEY}"):
        return jsonify({"error": "Invalid API key"}), 401
    
    data = request.json
    model = data.get("model", "openai/gpt-3.5-turbo")
    messages = data.get("messages", [])
    
    # Get user prompt
    user_prompt = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_prompt = msg.get("content", "")
            break
    
    # Generate mock response
    responses = [
        "This is a simulated response from the mock API.",
        "I'm a mock AI assistant helping you test your workflow.",
        "Docker containers make deployment easy and consistent!",
        "LLMs are transforming how we build applications.",
    ]
    response_text = random.choice(responses)
    
    # Simulate processing delay
    time.sleep(random.uniform(0.1, 0.3))
    
    completion_id = f"cmpl-{hashlib.md5(f'{time.time()}'.encode()).hexdigest()[:8]}"
    
    return jsonify({
        "id": completion_id,
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response_text
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }), 200

if __name__ == "__main__":
    print("🚀 Mock OpenRouter API starting...")
    print(f"   Health: http://0.0.0.0:8000/health")
    print(f"   Models: http://0.0.0.0:8000/api/v1/models")
    app.run(host="0.0.0.0", port=8000, debug=False)
