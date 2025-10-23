"""Enhanced Mock OpenRouter API Server"""
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import time
import random
import hashlib
import json
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)
CORS(app)

# Configuration
SIMULATED_API_KEY = os.getenv("SIMULATED_API_KEY", "sk-simulated-key")
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"

# Metrics
if ENABLE_METRICS:
    request_count = Counter('mock_api_requests_total', 'Total requests', ['endpoint', 'status'])
    request_duration = Histogram('mock_api_request_duration_seconds', 'Request duration', ['endpoint'])

# Response templates
RESPONSE_TEMPLATES = {
    "haiku": [
        "Containers drift by,\nIsolated yet connected,\nDocker's symphony.",
        "Code flows like water,\nThrough pipelines and registries,\nDevOps harmony.",
        "Microservices dance,\nOrchestrated by the cloud,\nScaling endlessly."
    ],
    "test": [
        "✅ Test successful! Mock API is working correctly.",
        "🎯 Mock API responding normally. All systems operational.",
        "🚀 Test passed! Ready for workflow execution."
    ],
    "error": [
        "❌ Simulated error for testing error handling.",
        "⚠️ Warning: This is a test error response.",
        "🔥 Critical: Simulated failure scenario."
    ]
}

def track_request(endpoint):
    """Decorator to track requests"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                if ENABLE_METRICS:
                    request_count.labels(endpoint=endpoint, status='success').inc()
                return result
            except Exception as e:
                if ENABLE_METRICS:
                    request_count.labels(endpoint=endpoint, status='error').inc()
                raise
            finally:
                if ENABLE_METRICS:
                    duration = time.time() - start
                    request_duration.labels(endpoint=endpoint).observe(duration)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0"
    }), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    """Prometheus metrics endpoint"""
    if ENABLE_METRICS:
        return Response(generate_latest(), mimetype='text/plain')
    return "Metrics disabled", 404

@app.route("/api/v1/chat/completions", methods=["POST"])
@track_request("chat_completions")
def chat_completions():
    """Mock OpenRouter chat completions endpoint"""
    
    # Validate API key
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith(f"Bearer {SIMULATED_API_KEY}"):
        return jsonify({"error": "Invalid API key"}), 401
    
    # Parse request
    data = request.json
    model = data.get("model", "openai/gpt-3.5-turbo")
    messages = data.get("messages", [])
    temperature = data.get("temperature", 0.7)
    max_tokens = data.get("max_tokens", 150)
    stream = data.get("stream", False)
    
    # Extract user prompt
    user_prompt = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_prompt = msg.get("content", "")
            break
    
    # Generate response based on prompt
    response_text = generate_response(user_prompt, model, temperature)
    
    # Simulate processing delay
    time.sleep(random.uniform(0.1, 0.5))
    
    # Create response
    completion_id = f"cmpl-{hashlib.md5(f'{time.time()}'.encode()).hexdigest()[:8]}"
    
    if stream:
        # SSE streaming response
        def generate():
            chunks = response_text.split(' ')
            for chunk in chunks:
                data = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "delta": {"content": chunk + " "},
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(data)}\n\n"
                time.sleep(0.05)
            
            # Final chunk
            data["choices"][0]["delta"] = {}
            data["choices"][0]["finish_reason"] = "stop"
            yield f"data: {json.dumps(data)}\n\n"
            yield "data: [DONE]\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    # Normal response
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
            "prompt_tokens": len(user_prompt.split()),
            "completion_tokens": len(response_text.split()),
            "total_tokens": len(user_prompt.split()) + len(response_text.split())
        }
    })

def generate_response(prompt: str, model: str, temperature: float) -> str:
    """Generate mock response based on prompt"""
    prompt_lower = prompt.lower()
    
    # Check for specific keywords
    if "haiku" in prompt_lower:
        responses = RESPONSE_TEMPLATES["haiku"]
    elif "test" in prompt_lower:
        responses = RESPONSE_TEMPLATES["test"]
    elif "error" in prompt_lower or "fail" in prompt_lower:
        responses = RESPONSE_TEMPLATES["error"]
    else:
        # Generate contextual response
        return f"Mock response from {model}: Received prompt '{prompt[:50]}...' | Temperature: {temperature:.2f} | This is a simulated response for testing purposes."
    
    # Return random response from template
    return random.choice(responses)

@app.route("/api/v1/models", methods=["GET"])
@track_request("list_models")
def list_models():
    """List available models"""
    return jsonify({
        "object": "list",
        "data": [
            {"id": "openai/gpt-3.5-turbo", "object": "model", "created": 1677649963, "owned_by": "openai"},
            {"id": "openai/gpt-4", "object": "model", "created": 1687882411, "owned_by": "openai"},
            {"id": "anthropic/claude-2", "object": "model", "created": 1689095500, "owned_by": "anthropic"},
            {"id": "google/palm-2", "object": "model", "created": 1683756000, "owned_by": "google"},
            {"id": "meta-llama/llama-2-70b", "object": "model", "created": 1689638400, "owned_by": "meta"}
        ]
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🚀 Mock API Server starting on port {port}")
    print(f"🔑 Using API key: {SIMULATED_API_KEY}")
    print(f"📊 Metrics enabled: {ENABLE_METRICS}")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
