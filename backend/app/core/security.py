"""
Security utilities for the Autonomous Research System.

This module handles authentication, authorization, password hashing,
JWT token management, and security-related utilities.
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import hashlib
import logging

from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()


class SecurityManager:
    """Security manager for authentication and authorization."""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)
    
    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.warning(f"JWT token verification failed: {e}")
            return None
    
    def create_tokens(self, user_id: int, email: str, roles: list = None) -> dict:
        """Create both access and refresh tokens for a user."""
        data = {
            "sub": str(user_id),
            "email": email,
            "roles": roles or ["user"]
        }
        
        access_token = self.create_access_token(data=data)
        refresh_token = self.create_refresh_token(data=data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60
        }
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Create a new access token using a refresh token."""
        payload = self.verify_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            return None
        
        # Create new access token with same user data
        access_data = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "roles": payload.get("roles", ["user"])
        }
        
        return self.create_access_token(data=access_data)
    
    def generate_api_key(self) -> str:
        """Generate a secure API key."""
        return secrets.token_urlsafe(32)
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash an API key for storage."""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def verify_api_key(self, api_key: str, hashed_api_key: str) -> bool:
        """Verify an API key against its hash."""
        return self.hash_api_key(api_key) == hashed_api_key


# Global security manager instance
security_manager = SecurityManager()


class AuthDependencies:
    """Authentication dependencies for FastAPI."""
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> dict:
        """Get current user from JWT token."""
        token = credentials.credentials
        payload = security_manager.verify_token(token)
        
        if not payload or payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "id": int(user_id),
            "email": payload.get("email"),
            "roles": payload.get("roles", ["user"])
        }
    
    @staticmethod
    async def get_current_active_user(
        current_user: dict = Depends(AuthDependencies.get_current_user)
    ) -> dict:
        """Get current active user."""
        # Here you would typically check if the user is active in the database
        # For now, we'll assume all authenticated users are active
        return current_user
    
    @staticmethod
    async def require_roles(required_roles: list):
        """Dependency to require specific roles."""
        async def role_checker(
            current_user: dict = Depends(AuthDependencies.get_current_user)
        ) -> dict:
            user_roles = current_user.get("roles", [])
            
            if not any(role in user_roles for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return current_user
        
        return role_checker
    
    @staticmethod
    async def require_admin(
        current_user: dict = Depends(AuthDependencies.get_current_user)
    ) -> dict:
        """Require admin role."""
        if "admin" not in current_user.get("roles", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user


class RateLimiter:
    """Rate limiting utilities."""
    
    def __init__(self):
        self.request_counts = {}
    
    def is_rate_limited(self, identifier: str, limit: int, window: int) -> bool:
        """Check if a request is rate limited."""
        now = datetime.utcnow()
        key = f"{identifier}:{window}"
        
        if key not in self.request_counts:
            self.request_counts[key] = []
        
        # Remove old requests outside the window
        self.request_counts[key] = [
            timestamp for timestamp in self.request_counts[key]
            if (now - timestamp).seconds < window
        ]
        
        # Check if limit exceeded
        if len(self.request_counts[key]) >= limit:
            return True
        
        # Add current request
        self.request_counts[key].append(now)
        return False
    
    def get_remaining_requests(self, identifier: str, limit: int, window: int) -> int:
        """Get remaining requests for an identifier."""
        now = datetime.utcnow()
        key = f"{identifier}:{window}"
        
        if key not in self.request_counts:
            return limit
        
        # Remove old requests outside the window
        self.request_counts[key] = [
            timestamp for timestamp in self.request_counts[key]
            if (now - timestamp).seconds < window
        ]
        
        return max(0, limit - len(self.request_counts[key]))


# Global rate limiter instance
rate_limiter = RateLimiter()


class SecurityUtils:
    """Security utility functions."""
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Basic sanitization - in production, use a proper library
        dangerous_chars = ["<", ">", "'", '"', "&", ";", "--", "/*", "*/"]
        sanitized = input_string
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        return sanitized.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """Validate password strength."""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain at least one special character")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def generate_secure_filename(original_filename: str) -> str:
        """Generate a secure filename."""
        import os
        from datetime import datetime
        
        # Get file extension
        _, ext = os.path.splitext(original_filename)
        
        # Generate secure name
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        random_suffix = secrets.token_hex(8)
        
        return f"{timestamp}_{random_suffix}{ext}"
    
    @staticmethod
    def is_safe_file_type(filename: str, allowed_types: list) -> bool:
        """Check if file type is allowed."""
        import os
        _, ext = os.path.splitext(filename.lower())
        return ext in allowed_types


# Export commonly used items
__all__ = [
    "SecurityManager",
    "security_manager",
    "AuthDependencies",
    "RateLimiter",
    "rate_limiter",
    "SecurityUtils",
    "pwd_context",
]
