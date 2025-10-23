"""Action registry for LLMs_OS"""
from typing import Dict, Callable, Any, List

# Global registry
_ACTION_REGISTRY: Dict[str, Callable] = {}

def register(action_name: str):
    """Decorator to register an action"""
    def decorator(func: Callable):
        _ACTION_REGISTRY[action_name] = func
        return func
    return decorator

def get_action(action_name: str) -> Callable:
    """Get action function by name"""
    return _ACTION_REGISTRY.get(action_name)

def list_actions() -> List[str]:
    """List all registered actions"""
    return list(_ACTION_REGISTRY.keys())

def action_exists(action_name: str) -> bool:
    """Check if action exists"""
    return action_name in _ACTION_REGISTRY
