"""
Dependency Injection
Shared dependencies for FastAPI endpoints
"""
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from app.config import settings
from app.security.auth import verify_token

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials = Depends(security)
) -> dict:
    """
    Verify and get current authenticated user
    """
    try:
        user = verify_token(credentials.credentials)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_doctor(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Get current authenticated doctor user
    Ensures user has doctor role
    """
    if current_user.get("role") != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors can access this resource"
        )
    return current_user


async def get_current_admin(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Get current authenticated admin user
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
