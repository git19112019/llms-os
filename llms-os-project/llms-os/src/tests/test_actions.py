"""Tests for actions"""
import pytest
from LLMs_OS.actions.print_message import print_message_action
from LLMs_OS.actions.file_operations import file_read_action, file_write_action

def test_print_message():
    """Test print message action"""
    result = print_message_action(
        {'message': 'Test message', 'style': 'info'},
        {}
    )
    assert result['last_message'] == 'Test message'

def test_file_operations(tmp_path):
    """Test file read/write"""
    test_file = tmp_path / "test.txt"
    content = "Hello, World!"
    
    # Write
    write_result = file_write_action(
        {'path': str(test_file), 'content': content},
        {}
    )
    assert write_result['path'] == str(test_file)
    
    # Read
    read_result = file_read_action(
        {'path': str(test_file)},
        {}
    )
    assert read_result['content'] == content
