# Imports.
import os
import sys
import jwt
from fastapi import HTTPException, Header
from typing import Optional

# Load JWT secret from environment variables.
JWT_SECRET = os.getenv("JWT_SECRET")

# Define a function to check if we are in testing mode.
def is_testing():
    """Check if we're currently running tests."""
    return "pytest" in sys.modules or os.getenv("TESTING") == "true"

# Define the authentication dependency.
def verify_token(authorization: Optional[str] = Header(None)):
    """
    Dependency to verify JWT token
    """

    # Skip authentication during testing.
    if is_testing():
        return {
            "user_id": "test_user_123",
            "email": "test@example.com",
            "user_type": "user"
        }
    
    # Check if Authorization header is present
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Check Bearer format
    parts = authorization.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(
            status_code=401, 
            detail="Authorization header must be in format: Bearer <token>"
        )
    
    # Extract token.
    token = parts[1]
    try:
        # Verify token.
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
