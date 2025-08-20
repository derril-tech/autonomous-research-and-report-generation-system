"""
Authentication endpoints for user registration, login, and token management
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from app.core.security import AuthDependencies, SecurityUtils
from app.core.dependencies import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    organization: str = None
    role: str = "researcher"


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Register a new user"""
    try:
        # Validate email format
        if not SecurityUtils.is_valid_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Validate password strength
        if not SecurityUtils.is_valid_password(request.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long and contain letters and numbers"
            )
        
        # Create user
        user_data = UserCreate(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            organization=request.organization,
            role=request.role
        )
        
        result = await auth_service.register_user(db, user_data)
        
        logger.info(f"User registered successfully: {request.email}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed for {request.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Authenticate user and return access token"""
    try:
        result = await auth_service.authenticate_user(
            db, 
            email=request.email, 
            password=request.password
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        logger.info(f"User logged in successfully: {request.email}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed for {request.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshRequest,
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Refresh access token using refresh token"""
    try:
        result = await auth_service.refresh_token(db, request.refresh_token)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        logger.info("Token refreshed successfully")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout(
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Logout user and invalidate tokens"""
    try:
        await auth_service.logout_user(db, current_user.id)
        
        logger.info(f"User logged out successfully: {current_user.email}")
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error(f"Logout failed for {current_user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user=Depends(AuthDependencies.get_current_user)
) -> Any:
    """Get current user information"""
    return current_user
