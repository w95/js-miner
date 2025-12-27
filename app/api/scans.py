"""Scan endpoints"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import logging

from app.models.schemas import (
    ScanRequest,
    BatchScanRequest,
    ScanResponse,
    ScanResult
)
from app.core.scanner_builder import ScannerBuilder


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=ScanResponse)
async def create_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Create a new scan for a single URL
    
    Args:
        request: Scan request with URL and scan types
        background_tasks: FastAPI background tasks
        
    Returns:
        Scan response with task IDs
    """
    try:
        logger.info(f"Creating scan for {request.url}")
        
        # Create scanner builder
        builder = ScannerBuilder(
            url=str(request.url),
            content=request.content,
            headers=request.headers or {}
        ).with_scan_types(request.scan_types)
        
        # Execute scans in background
        background_tasks.add_task(builder.execute)
        
        return ScanResponse(
            message=f"Scan initiated for {request.url}",
            task_ids=[],  # Tasks are created during execution
            task_count=len(request.scan_types)
        )
    except Exception as e:
        logger.error(f"Error creating scan: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=ScanResponse)
async def create_batch_scan(request: BatchScanRequest, background_tasks: BackgroundTasks):
    """
    Create scans for multiple URLs
    
    Args:
        request: Batch scan request with URLs and scan types
        background_tasks: FastAPI background tasks
        
    Returns:
        Scan response with task IDs
    """
    try:
        logger.info(f"Creating batch scan for {len(request.urls)} URLs")
        
        total_tasks = 0
        for url in request.urls:
            # Create scanner builder for each URL
            builder = ScannerBuilder(
                url=str(url),
                content=None,
                headers={}
            ).with_scan_types(request.scan_types)
            
            # Execute scans in background
            background_tasks.add_task(builder.execute)
            total_tasks += len(request.scan_types)
        
        return ScanResponse(
            message=f"Batch scan initiated for {len(request.urls)} URLs",
            task_ids=[],  # Tasks are created during execution
            task_count=total_tasks
        )
    except Exception as e:
        logger.error(f"Error creating batch scan: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/immediate", response_model=List[ScanResult])
async def execute_scan_immediate(request: ScanRequest):
    """
    Execute a scan immediately and return results
    
    Args:
        request: Scan request with URL and scan types
        
    Returns:
        List of scan results
    """
    try:
        logger.info(f"Executing immediate scan for {request.url}")
        
        # Create scanner builder
        builder = ScannerBuilder(
            url=str(request.url),
            content=request.content,
            headers=request.headers or {}
        ).with_scan_types(request.scan_types)
        
        # Execute scans immediately
        results = await builder.execute()
        
        return results
    except Exception as e:
        logger.error(f"Error executing immediate scan: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
