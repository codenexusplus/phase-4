from fastapi import HTTPException, status
from typing import Dict, Any


class BusinessError(Exception):
    """Custom exception for business logic errors"""
    def __init__(self, message: str, error_code: str = "BUSINESS_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


def handle_error(message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    """Helper function to raise HTTP exceptions with consistent format"""
    raise HTTPException(
        status_code=status_code,
        detail={
            "error": message,
            "code": status.HTTP_400_BAD_REQUEST
        }
    )


def create_error_response(message: str, error_code: str = "GENERIC_ERROR") -> Dict[str, Any]:
    """Create a standardized error response"""
    return {
        "error": message,
        "code": error_code
    }
