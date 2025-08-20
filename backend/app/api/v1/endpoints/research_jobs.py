"""
Research jobs endpoints for managing research job lifecycle
"""

from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.security import AuthDependencies
from app.core.dependencies import get_db, ValidationDependencies
from app.services.research_service import ResearchService
from app.schemas.research_job import (
    ResearchJobCreate, 
    ResearchJobUpdate, 
    ResearchJobResponse,
    ResearchJobList,
    JobProgressResponse,
    JobStatsResponse
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=ResearchJobResponse)
async def create_research_job(
    job_data: ResearchJobCreate,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Create a new research job"""
    try:
        result = await research_service.create_job(db, job_data, current_user.id)
        
        logger.info(f"Research job created: {result.job.id} by user {current_user.id}")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create research job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create research job"
        )


@router.get("/", response_model=ResearchJobList)
async def list_research_jobs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """List research jobs with pagination and filtering"""
    try:
        # Validate pagination parameters
        pagination = ValidationDependencies.validate_pagination(page, limit)
        sorting = ValidationDependencies.validate_sorting(sort_by, sort_order)
        
        result = await research_service.list_jobs(
            db,
            user_id=current_user.id,
            page=pagination.page,
            limit=pagination.limit,
            status=status,
            search=search,
            sort_by=sorting.sort_by,
            sort_order=sorting.sort_order
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to list research jobs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list research jobs"
        )


@router.get("/{job_id}", response_model=ResearchJobResponse)
async def get_research_job(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Get a specific research job"""
    try:
        result = await research_service.get_job(db, job_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get research job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get research job"
        )


@router.put("/{job_id}", response_model=ResearchJobResponse)
async def update_research_job(
    job_id: UUID,
    job_data: ResearchJobUpdate,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Update a research job"""
    try:
        result = await research_service.update_job(db, job_id, job_data, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        logger.info(f"Research job updated: {job_id} by user {current_user.id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update research job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update research job"
        )


@router.delete("/{job_id}")
async def delete_research_job(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Delete a research job (soft delete)"""
    try:
        success = await research_service.delete_job(db, job_id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        logger.info(f"Research job deleted: {job_id} by user {current_user.id}")
        
        return {"message": "Research job deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete research job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete research job"
        )


@router.post("/{job_id}/start")
async def start_research_job(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Start a research job"""
    try:
        result = await research_service.start_job(db, job_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        logger.info(f"Research job started: {job_id} by user {current_user.id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start research job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start research job"
        )


@router.post("/{job_id}/cancel")
async def cancel_research_job(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Cancel a research job"""
    try:
        success = await research_service.cancel_job(db, job_id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        logger.info(f"Research job cancelled: {job_id} by user {current_user.id}")
        
        return {"message": "Research job cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel research job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel research job"
        )


@router.post("/{job_id}/retry")
async def retry_research_job(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Retry a failed research job"""
    try:
        result = await research_service.retry_job(db, job_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found or cannot be retried"
            )
        
        logger.info(f"Research job retried: {job_id} by user {current_user.id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retry research job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retry research job"
        )


@router.get("/{job_id}/progress", response_model=JobProgressResponse)
async def get_job_progress(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Get research job progress"""
    try:
        result = await research_service.get_job_progress(db, job_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job progress {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job progress"
        )


@router.get("/{job_id}/stream")
async def stream_job_updates(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Stream real-time job updates via Server-Sent Events"""
    try:
        # Verify job exists and user has access
        job = await research_service.get_job(db, job_id, current_user.id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        async def event_generator():
            """Generate SSE events for job updates"""
            try:
                async for event in research_service.stream_job_updates(job_id):
                    yield f"data: {event}\n\n"
            except Exception as e:
                logger.error(f"Error in job stream {job_id}: {str(e)}")
                yield f"data: {{\"error\": \"Stream error\"}}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to stream job updates {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to stream job updates"
        )


@router.get("/{job_id}/sources")
async def get_job_sources(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Get sources for a research job"""
    try:
        result = await research_service.get_job_sources(db, job_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job sources {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job sources"
        )


@router.get("/{job_id}/claims")
async def get_job_claims(
    job_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Get claims for a research job"""
    try:
        result = await research_service.get_job_claims(db, job_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research job not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job claims {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job claims"
        )


@router.get("/stats/summary", response_model=JobStatsResponse)
async def get_job_stats(
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    research_service: ResearchService = Depends()
) -> Any:
    """Get research job statistics"""
    try:
        result = await research_service.get_job_stats(db, current_user.id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to get job stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job statistics"
        )
