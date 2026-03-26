"""
Authentication & Security Module
OAuth/OIDC and JWT token management
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext

from app.config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    
    Args:
        data: Token payload
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None


class OAuthProvider:
    """OAuth/OIDC provider integration"""
    
    @staticmethod
    async def get_user_info(access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user info from OAuth provider
        
        Args:
            access_token: OAuth access token
            
        Returns:
            User information
        """
        # Implementation would integrate with Azure AD, Google, etc.
        # This is a placeholder for the real implementation
        logger.info("Fetching user info from OAuth provider")
        return {
            "sub": "user-id",
            "email": "doctor@hospital.com",
            "name": "Dr. Name",
            "role": "doctor"
        }
