"""LLMs_OS - Enhanced Workflow Automation System"""
__version__ = "2.0.0"
__author__ = "LLMs_OS Team"

from .core import execute_yaml
from .cli import main
from .registry import register, get_action, list_actions

# Import actions to register them
from . import actions

__all__ = [
    'execute_yaml',
    'main',
    'register',
    'get_action',
    'list_actions'
]
