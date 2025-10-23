"""Custom exceptions for LLMs_OS"""

class LLMsOSError(Exception):
    """Base exception for all LLMs_OS errors"""
    pass

class ActionNotFoundError(LLMsOSError):
    """Raised when an action is not found in registry"""
    pass

class WorkflowExecutionError(LLMsOSError):
    """Raised when workflow execution fails"""
    pass

class ValidationError(LLMsOSError):
    """Raised when input validation fails"""
    pass

class APIError(LLMsOSError):
    """Raised when API calls fail"""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
