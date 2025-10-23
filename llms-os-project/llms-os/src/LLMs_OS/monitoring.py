"""Metrics and monitoring for LLMs_OS"""
import time
import functools
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Metrics
task_counter = Counter('llms_os_tasks_total', 'Total tasks executed', ['action', 'status'])
task_duration = Histogram('llms_os_task_duration_seconds', 'Task execution time', ['action'])
active_workflows = Gauge('llms_os_active_workflows', 'Currently running workflows')
api_calls = Counter('llms_os_api_calls_total', 'API calls made', ['endpoint', 'status'])

class MetricsCollector:
    """Collect and expose metrics"""
    
    @staticmethod
    def track_task(action: str):
        """Decorator to track task execution"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    task_counter.labels(action=action, status='success').inc()
                    return result
                except Exception as e:
                    task_counter.labels(action=action, status='error').inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    task_duration.labels(action=action).observe(duration)
            return wrapper
        return decorator
    
    @staticmethod
    def track_workflow():
        """Context manager for workflow tracking"""
        class WorkflowTracker:
            def __enter__(self):
                active_workflows.inc()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                active_workflows.dec()
        
        return WorkflowTracker()
    
    @staticmethod
    def get_metrics():
        """Export metrics in Prometheus format"""
        return generate_latest()
