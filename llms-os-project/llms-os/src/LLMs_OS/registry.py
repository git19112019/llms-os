"""Action registry for LLMs_OS"""

_ACTIONS = {}

def register(name):
    """Decorator to register an action"""
    def decorator(func):
        _ACTIONS[name] = func
        return func
    return decorator

def get_action(name):
    """Get an action by name"""
    if name not in _ACTIONS:
        raise KeyError(f"Action not found: {name}")
    return _ACTIONS[name]

def list_actions():
    """List all registered actions"""
    return list(_ACTIONS.keys())
