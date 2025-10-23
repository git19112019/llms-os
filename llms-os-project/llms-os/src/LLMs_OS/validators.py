"""Input validation and sanitization"""
import re
from typing import Any, Dict, List
from .exceptions import ValidationError

class TaskValidator:
    """Validate task configurations"""
    
    REQUIRED_FIELDS = ['action']
    VALID_ACTIONS = None  # Populated from registry
    
    @classmethod
    def validate(cls, task: Dict[str, Any]) -> bool:
        """Validate a task dictionary"""
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in task:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate action exists
        action = task.get('action')
        if cls.VALID_ACTIONS and action not in cls.VALID_ACTIONS:
            raise ValidationError(f"Unknown action: {action}")
        
        # Sanitize string inputs
        for key, value in task.items():
            if isinstance(value, str):
                task[key] = cls.sanitize_string(value)
        
        return True
    
    @staticmethod
    def sanitize_string(value: str) -> str:
        """Remove potentially dangerous characters"""
        # Remove null bytes
        value = value.replace('\0', '')
        # Limit length
        return value[:10000]

class WorkflowValidator:
    """Validate entire workflow"""
    
    @staticmethod
    def validate(workflow: Dict[str, Any]) -> bool:
        """Validate workflow structure"""
        if 'tasks' not in workflow:
            raise ValidationError("Workflow must contain 'tasks' field")
        
        tasks = workflow.get('tasks', [])
        if not isinstance(tasks, list):
            raise ValidationError("Tasks must be a list")
        
        for idx, task in enumerate(tasks):
            try:
                TaskValidator.validate(task)
            except ValidationError as e:
                raise ValidationError(f"Task {idx + 1}: {e}")
        
        return True
