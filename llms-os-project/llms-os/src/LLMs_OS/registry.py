"""Action registry for LLMs OS"""
from typing import Dict, Callable, Any

_actions: Dict[str, Callable] = {}

def register(name: str):
    """Decorator to register an action"""
    def decorator(func: Callable) -> Callable:
        _actions[name] = func
        return func
    return decorator

def get_action(name: str) -> Callable:
    """Get an action by name"""
    return _actions.get(name)

def list_actions() -> list:
    """List all registered actions"""
    return list(_actions.keys())
