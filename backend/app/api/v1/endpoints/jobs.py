"""
Jobs API endpoints for research job management
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.job import Job, JobStatus
from app.schemas.job import JobCreate, JobResponse, JobUpdate, JobStatusResponse
from app.services.job_service import JobService
from app.services.langgraph_service import LangGraphService

router = APIRouter()


@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new research job"""
    job_service = JobService(db)
    langgraph_service = LangGraphService()
    
    # Create job in database
    job = await job_service.create_job(
        user_id=current_user.id,
        query=job_data.query,
        constraints=job_data.constraints,
        output_config=job_data.output,
        hil_config=job_data.hil
    )
    
    # Start LangGraph workflow in background
    background_tasks.add_task(
        langgraph_service.start_research_workflow,
        job_id=job.id,
        query=job_data.query,
        constraints=job_data.constraints,
        output_config=job_data.output,
        hil_config=job_data.hil
    )
    
    return JobResponse.from_orm(job)


@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get job status and progress"""
    job_service = JobService(db)
    
    job = await job_service.get_job_by_id(job_id, current_user.id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get progress information
    progress = await job_service.get_job_progress(job_id)
    
    return JobStatusResponse(
        id=job.id,
        status=job.status,
        progress=progress,
        links=await job_service.get_job_links(job_id),
        issues=await job_service.get_job_issues(job_id)
    )


@router.post("/{job_id}/review")
async def submit_review(
    job_id: UUID,
    review_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit human-in-the-loop review"""
    job_service = JobService(db)
    langgraph_service = LangGraphService()
    
    job = await job_service.get_job_by_id(job_id, current_user.id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Process review
    await langgraph_service.process_review(
        job_id=job_id,
        action=review_data.get("action"),
        instructions=review_data.get("instructions")
    )
    
    return {"message": "Review submitted successfully"}


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    status: Optional[JobStatus] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's jobs with optional filtering"""
    job_service = JobService(db)
    
    jobs = await job_service.list_user_jobs(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status
    )
    
    return [JobResponse.from_orm(job) for job in jobs]


@router.delete("/{job_id}")
async def cancel_job(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Cancel a running job"""
    job_service = JobService(db)
    langgraph_service = LangGraphService()
    
    job = await job_service.get_job_by_id(job_id, current_user.id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
        raise HTTPException(status_code=400, detail="Cannot cancel completed or failed job")
    
    # Cancel LangGraph workflow
    await langgraph_service.cancel_workflow(job_id)
    
    # Update job status
    await job_service.update_job_status(job_id, JobStatus.FAILED)
    
    return {"message": "Job cancelled successfully"}
