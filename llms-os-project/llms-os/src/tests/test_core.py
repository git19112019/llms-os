"""Tests for core functionality"""
import pytest
from LLMs_OS.core import render, execute_yaml
from LLMs_OS.registry import register, get_action

def test_render_simple():
    """Test simple template rendering"""
    result = render("Hello {{ name }}", {"name": "World"})
    assert result == "Hello World"

def test_render_env():
    """Test environment variable rendering"""
    result = render("Log level: {{ env.LOG_LEVEL }}", {"env": {"LOG_LEVEL": "INFO"}})
    assert result == "Log level: INFO"

def test_action_registration():
    """Test action registration"""
    @register('test_action')
    def test_func(task, context):
        return {'result': 'ok'}
    
    action = get_action('test_action')
    assert action is not None
    assert action({'action': 'test_action'}, {}) == {'result': 'ok'}
