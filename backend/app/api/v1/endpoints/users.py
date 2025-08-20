"""
Users endpoints for user profile management and activity tracking
"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from app.core.security import AuthDependencies
from app.core.dependencies import get_db, ValidationDependencies
from app.services.auth_service import AuthService
from app.schemas.user import UserUpdate, UserResponse, UserActivityList
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Get current user profile"""
    try:
        result = await auth_service.get_user_profile(db, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdate,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Update current user profile"""
    try:
        result = await auth_service.update_user_profile(db, current_user.id, user_data)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        logger.info(f"User profile updated: {current_user.id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.get("/activity", response_model=UserActivityList)
async def get_user_activity(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    activity_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Get user activity history"""
    try:
        # Validate pagination parameters
        pagination = ValidationDependencies.validate_pagination(page, limit)
        
        result = await auth_service.get_user_activity(
            db,
            user_id=current_user.id,
            page=pagination.page,
            limit=pagination.limit,
            activity_type=activity_type,
            start_date=start_date,
            end_date=end_date
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get user activity: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user activity"
        )


@router.get("/stats")
async def get_user_stats(
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Get user statistics"""
    try:
        result = await auth_service.get_user_stats(db, current_user.id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to get user stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user statistics"
        )


@router.post("/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Update user preferences"""
    try:
        result = await auth_service.update_user_preferences(
            db, 
            current_user.id, 
            preferences
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User preferences updated: {current_user.id}")
        
        return {"message": "Preferences updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user preferences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user preferences"
        )


@router.get("/usage")
async def get_user_usage(
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Get user usage statistics"""
    try:
        result = await auth_service.get_user_usage(db, current_user.id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to get user usage: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user usage statistics"
        )


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Change user password"""
    try:
        success = await auth_service.change_password(
            db,
            current_user.id,
            current_password,
            new_password
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        logger.info(f"Password changed for user: {current_user.id}")
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to change password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.post("/deactivate")
async def deactivate_account(
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    auth_service: AuthService = Depends()
) -> Any:
    """Deactivate user account"""
    try:
        success = await auth_service.deactivate_account(db, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"Account deactivated: {current_user.id}")
        
        return {"message": "Account deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to deactivate account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate account"
        )
