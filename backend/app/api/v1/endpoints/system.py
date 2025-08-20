"""
System endpoints for health checks, metrics, and monitoring
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.dependencies import get_db
from app.services.system_service import SystemService
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check(
    db=Depends(get_db),
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """System health check endpoint"""
    try:
        result = await system_service.health_check(db)
        return result
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "error": str(e)
        }


@router.get("/metrics")
async def get_metrics(
    current_user=Depends(AuthDependencies.get_current_user),
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """Get system metrics"""
    try:
        result = await system_service.get_metrics()
        return result
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system metrics"
        )


@router.get("/status")
async def system_status(
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """Get system status information"""
    try:
        result = await system_service.get_status()
        return result
        
    except Exception as e:
        logger.error(f"Failed to get system status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system status"
        )


@router.get("/info")
async def system_info() -> Dict[str, Any]:
    """Get system information"""
    try:
        return {
            "name": "Autonomous Research & Report Generation System",
            "version": "1.0.0",
            "description": "AI-powered platform for automated research and report generation",
            "features": [
                "Multi-agent AI orchestration",
                "Real-time progress tracking",
                "Multiple export formats",
                "Enterprise security",
                "Scalable architecture"
            ],
            "technology_stack": {
                "backend": "FastAPI + Python 3.11+",
                "frontend": "Next.js 14 + React 18",
                "database": "PostgreSQL + pgvector",
                "ai_workflow": "LangGraph + LangChain",
                "cache": "Redis",
                "storage": "S3/GCS"
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get system info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system information"
        )


@router.get("/config")
async def system_config(
    current_user=Depends(AuthDependencies.get_current_user),
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """Get system configuration (non-sensitive)"""
    try:
        result = await system_service.get_config(current_user.id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to get system config: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system configuration"
        )


@router.post("/maintenance")
async def trigger_maintenance(
    maintenance_type: str,
    current_user=Depends(AuthDependencies.get_current_user),
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """Trigger system maintenance tasks (admin only)"""
    try:
        # Check if user is admin
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        result = await system_service.trigger_maintenance(maintenance_type)
        
        logger.info(f"Maintenance triggered: {maintenance_type} by user {current_user.id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger maintenance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger maintenance"
        )


@router.get("/logs")
async def get_system_logs(
    level: str = "INFO",
    limit: int = 100,
    current_user=Depends(AuthDependencies.get_current_user),
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """Get system logs (admin only)"""
    try:
        # Check if user is admin
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        result = await system_service.get_logs(level, limit)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get system logs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system logs"
        )


@router.get("/performance")
async def get_performance_metrics(
    current_user=Depends(AuthDependencies.get_current_user),
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """Get system performance metrics"""
    try:
        result = await system_service.get_performance_metrics()
        return result
        
    except Exception as e:
        logger.error(f"Failed to get performance metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get performance metrics"
        )


@router.get("/alerts")
async def get_system_alerts(
    current_user=Depends(AuthDependencies.get_current_user),
    system_service: SystemService = Depends()
) -> Dict[str, Any]:
    """Get system alerts and notifications"""
    try:
        result = await system_service.get_alerts(current_user.id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to get system alerts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system alerts"
        )
