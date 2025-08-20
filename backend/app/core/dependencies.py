"""
Common dependencies for the Autonomous Research System.

This module provides reusable FastAPI dependencies for database sessions,
authentication, rate limiting, and other common functionality.
"""

from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from .database import get_db, db_manager
from .security import security_manager, rate_limiter, AuthDependencies
from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Security scheme
security = HTTPBearer()


class Dependencies:
    """Common FastAPI dependencies."""
    
    @staticmethod
    async def get_database():
        """Database session dependency."""
        async for session in get_db():
            yield session
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> dict:
        """Get current authenticated user."""
        return await AuthDependencies.get_current_user(credentials)
    
    @staticmethod
    async def get_current_active_user(
        current_user: dict = Depends(get_current_user)
    ) -> dict:
        """Get current active user."""
        return await AuthDependencies.get_current_active_user(current_user)
    
    @staticmethod
    async def require_admin(
        current_user: dict = Depends(get_current_user)
    ) -> dict:
        """Require admin role."""
        return await AuthDependencies.require_admin(current_user)
    
    @staticmethod
    async def require_roles(required_roles: list):
        """Dependency factory for role-based access control."""
        return await AuthDependencies.require_roles(required_roles)
    
    @staticmethod
    async def rate_limit(
        request: Request,
        limit: int = settings.RATE_LIMIT_PER_MINUTE,
        window: int = 60
    ):
        """Rate limiting dependency."""
        # Get client identifier (IP address or user ID)
        client_id = request.client.host
        
        if rate_limiter.is_rate_limited(client_id, limit, window):
            remaining = rate_limiter.get_remaining_requests(client_id, limit, window)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {window} seconds.",
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": str(remaining),
                    "X-RateLimit-Reset": str(window)
                }
            )
        
        return True
    
    @staticmethod
    async def check_database_health():
        """Check database connectivity."""
        is_healthy = await db_manager.health_check()
        if not is_healthy:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed"
            )
        return True
    
    @staticmethod
    async def get_user_context(
        current_user: dict = Depends(get_current_user),
        db = Depends(get_database)
    ) -> dict:
        """Get user context with database session."""
        return {
            "user": current_user,
            "db": db
        }


class OptionalDependencies:
    """Optional dependencies that don't raise exceptions."""
    
    @staticmethod
    async def get_optional_user(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> Optional[dict]:
        """Get current user if authenticated, None otherwise."""
        if not credentials:
            return None
        
        try:
            return await AuthDependencies.get_current_user(credentials)
        except HTTPException:
            return None
    
    @staticmethod
    async def get_optional_database():
        """Get database session if available."""
        try:
            async for session in get_db():
                yield session
        except Exception as e:
            logger.warning(f"Database session not available: {e}")
            yield None


class ValidationDependencies:
    """Dependencies for input validation."""
    
    @staticmethod
    def validate_pagination(
        page: int = 1,
        size: int = 20,
        max_size: int = 100
    ) -> dict:
        """Validate pagination parameters."""
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page number must be greater than 0"
            )
        
        if size < 1 or size > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Page size must be between 1 and {max_size}"
            )
        
        return {"page": page, "size": size}
    
    @staticmethod
    def validate_sorting(
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        allowed_fields: list = None
    ) -> dict:
        """Validate sorting parameters."""
        if sort_by and allowed_fields and sort_by not in allowed_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field. Allowed: {', '.join(allowed_fields)}"
            )
        
        if sort_order.lower() not in ["asc", "desc"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sort order must be 'asc' or 'desc'"
            )
        
        return {
            "sort_by": sort_by,
            "sort_order": sort_order.lower()
        }


class MonitoringDependencies:
    """Dependencies for monitoring and observability."""
    
    @staticmethod
    async def log_request(
        request: Request,
        response_time: float = 0.0
    ):
        """Log request details for monitoring."""
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Status: {getattr(request, 'status_code', 'N/A')} "
            f"Response Time: {response_time:.3f}s "
            f"Client: {request.client.host}"
        )
    
    @staticmethod
    async def track_metrics(
        request: Request,
        operation: str,
        success: bool = True
    ):
        """Track metrics for monitoring."""
        # In a real implementation, you would send metrics to your monitoring system
        logger.info(
            f"Metrics: {operation} "
            f"Success: {success} "
            f"Path: {request.url.path} "
            f"Method: {request.method}"
        )


class CacheDependencies:
    """Dependencies for caching."""
    
    @staticmethod
    async def get_cache_key(
        prefix: str,
        user_id: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate cache key."""
        key_parts = [prefix]
        
        if user_id:
            key_parts.append(f"user:{user_id}")
        
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        return ":".join(key_parts)
    
    @staticmethod
    async def get_cache_ttl(
        cache_type: str = "default",
        user_role: str = "user"
    ) -> int:
        """Get cache TTL based on type and user role."""
        ttl_map = {
            "default": 300,  # 5 minutes
            "user_data": 600,  # 10 minutes
            "search_results": 1800,  # 30 minutes
            "reports": 3600,  # 1 hour
            "admin": 7200,  # 2 hours for admin users
        }
        
        base_ttl = ttl_map.get(cache_type, ttl_map["default"])
        
        # Admin users get longer cache times
        if user_role == "admin":
            base_ttl = ttl_map.get("admin", base_ttl)
        
        return base_ttl


# Convenience functions for common dependency combinations
async def get_authenticated_user_with_db():
    """Get authenticated user with database session."""
    async def dependency(
        current_user: dict = Depends(Dependencies.get_current_user),
        db = Depends(Dependencies.get_database)
    ):
        return {"user": current_user, "db": db}
    
    return dependency


async def get_admin_user_with_db():
    """Get admin user with database session."""
    async def dependency(
        current_user: dict = Depends(Dependencies.require_admin),
        db = Depends(Dependencies.get_database)
    ):
        return {"user": current_user, "db": db}
    
    return dependency


# Export commonly used dependencies
__all__ = [
    "Dependencies",
    "OptionalDependencies",
    "ValidationDependencies",
    "MonitoringDependencies",
    "CacheDependencies",
    "get_authenticated_user_with_db",
    "get_admin_user_with_db",
]
