"""Task management endpoints"""
from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID
import logging

from app.models.schemas import TaskInfo, TaskSummary, TaskStatus
from app.core.task_repository import task_repository


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/summary", response_model=TaskSummary)
async def get_task_summary():
    """
    Get summary of all tasks
    
    Returns:
        Task summary with counts
    """
    try:
        summary = await task_repository.get_task_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting task summary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[TaskInfo])
async def get_all_tasks():
    """
    Get all tasks
    
    Returns:
        List of all tasks
    """
    try:
        tasks = await task_repository.get_all_tasks()
        return tasks
    except Exception as e:
        logger.error(f"Error getting all tasks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", response_model=TaskInfo)
async def get_task(task_id: UUID):
    """
    Get task by ID
    
    Args:
        task_id: Task UUID
        
    Returns:
        Task information
    """
    try:
        task = await task_repository.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{status}", response_model=List[TaskInfo])
async def get_tasks_by_status(status: TaskStatus):
    """
    Get tasks by status
    
    Args:
        status: Task status to filter by
        
    Returns:
        List of tasks with given status
    """
    try:
        tasks = await task_repository.get_tasks_by_status(status)
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks by status {status}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/completed")
async def clear_completed_tasks():
    """
    Clear all completed tasks
    
    Returns:
        Success message
    """
    try:
        await task_repository.clear_completed_tasks()
        return {"message": "Completed tasks cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing completed tasks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
