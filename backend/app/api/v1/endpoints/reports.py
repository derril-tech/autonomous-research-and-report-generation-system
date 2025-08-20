"""
Reports endpoints for managing generated reports
"""

from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.core.security import AuthDependencies
from app.core.dependencies import get_db, ValidationDependencies
from app.services.report_service import ReportService
from app.schemas.report import ReportResponse, ReportList
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=ReportList)
async def list_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    job_id: Optional[UUID] = Query(None),
    format: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    report_service: ReportService = Depends()
) -> Any:
    """List reports with pagination and filtering"""
    try:
        # Validate pagination parameters
        pagination = ValidationDependencies.validate_pagination(page, limit)
        sorting = ValidationDependencies.validate_sorting(sort_by, sort_order)
        
        result = await report_service.list_reports(
            db,
            user_id=current_user.id,
            page=pagination.page,
            limit=pagination.limit,
            job_id=job_id,
            format=format,
            search=search,
            sort_by=sorting.sort_by,
            sort_order=sorting.sort_order
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to list reports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list reports"
        )


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    report_service: ReportService = Depends()
) -> Any:
    """Get a specific report"""
    try:
        result = await report_service.get_report(db, report_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get report {report_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get report"
        )


@router.get("/{report_id}/download")
async def download_report(
    report_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    report_service: ReportService = Depends()
) -> Any:
    """Download a report file"""
    try:
        file_path = await report_service.get_report_file(db, report_id, current_user.id)
        
        if not file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report file not found"
            )
        
        # Increment download count
        await report_service.increment_download_count(db, report_id)
        
        return FileResponse(
            path=file_path,
            filename=f"report_{report_id}.pdf",
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to download report {report_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download report"
        )


@router.post("/{report_id}/export")
async def export_report(
    report_id: UUID,
    format: str = Query(..., regex="^(pdf|docx|pptx)$"),
    include_appendices: bool = Query(False),
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    report_service: ReportService = Depends()
) -> Any:
    """Export report in different format"""
    try:
        result = await report_service.export_report(
            db, 
            report_id, 
            current_user.id, 
            format, 
            include_appendices
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        logger.info(f"Report exported: {report_id} to {format} by user {current_user.id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export report {report_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export report"
        )


@router.post("/{report_id}/publish")
async def publish_report(
    report_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    report_service: ReportService = Depends()
) -> Any:
    """Publish a report (make it publicly accessible)"""
    try:
        result = await report_service.publish_report(db, report_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        logger.info(f"Report published: {report_id} by user {current_user.id}")
        
        return {"message": "Report published successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to publish report {report_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish report"
        )


@router.post("/{report_id}/unpublish")
async def unpublish_report(
    report_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    report_service: ReportService = Depends()
) -> Any:
    """Unpublish a report (make it private)"""
    try:
        result = await report_service.unpublish_report(db, report_id, current_user.id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        logger.info(f"Report unpublished: {report_id} by user {current_user.id}")
        
        return {"message": "Report unpublished successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to unpublish report {report_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unpublish report"
        )


@router.delete("/{report_id}")
async def delete_report(
    report_id: UUID,
    current_user=Depends(AuthDependencies.get_current_user),
    db=Depends(get_db),
    report_service: ReportService = Depends()
) -> Any:
    """Delete a report"""
    try:
        success = await report_service.delete_report(db, report_id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        logger.info(f"Report deleted: {report_id} by user {current_user.id}")
        
        return {"message": "Report deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete report {report_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete report"
        )
