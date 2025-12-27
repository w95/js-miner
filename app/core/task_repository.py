"""Task repository for managing scan tasks"""
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4
import logging

from app.models.schemas import TaskInfo, TaskStatus, TaskName, TaskSummary


logger = logging.getLogger(__name__)


class TaskRepository:
    """Repository for managing scan tasks"""
    
    def __init__(self):
        """Initialize task repository"""
        self.tasks: Dict[UUID, TaskInfo] = {}
        self.lock = asyncio.Lock()
        self._shutdown = False
    
    async def create_task(self, url: str, task_name: TaskName) -> UUID:
        """
        Create a new task
        
        Args:
            url: URL being scanned
            task_name: Type of scan task
            
        Returns:
            Task UUID
        """
        task_id = uuid4()
        task_info = TaskInfo(
            task_id=task_id,
            url=url,
            task_name=task_name,
            status=TaskStatus.QUEUED,
            created_at=datetime.now(),
            started_at=None,
            completed_at=None
        )
        
        async with self.lock:
            self.tasks[task_id] = task_info
        
        logger.info(f"Created task {task_id} for {task_name.value} on {url}")
        return task_id
    
    async def start_task(self, task_id: UUID):
        """
        Mark task as running
        
        Args:
            task_id: Task UUID
        """
        async with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.RUNNING
                self.tasks[task_id].started_at = datetime.now()
                logger.debug(f"Started task {task_id}")
    
    async def complete_task(self, task_id: UUID):
        """
        Mark task as completed
        
        Args:
            task_id: Task UUID
        """
        async with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.COMPLETED
                self.tasks[task_id].completed_at = datetime.now()
                logger.debug(f"Completed task {task_id}")
    
    async def fail_task(self, task_id: UUID):
        """
        Mark task as failed
        
        Args:
            task_id: Task UUID
        """
        async with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.FAILED
                self.tasks[task_id].completed_at = datetime.now()
                logger.warning(f"Failed task {task_id}")
    
    async def skip_task(self, task_id: UUID):
        """
        Mark task as skipped (duplicate)
        
        Args:
            task_id: Task UUID
        """
        async with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.SKIPPED
                self.tasks[task_id].completed_at = datetime.now()
                logger.debug(f"Skipped task {task_id}")
    
    async def get_task(self, task_id: UUID) -> Optional[TaskInfo]:
        """
        Get task by ID
        
        Args:
            task_id: Task UUID
            
        Returns:
            TaskInfo or None
        """
        async with self.lock:
            return self.tasks.get(task_id)
    
    async def get_all_tasks(self) -> List[TaskInfo]:
        """
        Get all tasks
        
        Returns:
            List of all tasks
        """
        async with self.lock:
            return list(self.tasks.values())
    
    async def get_tasks_by_status(self, status: TaskStatus) -> List[TaskInfo]:
        """
        Get tasks by status
        
        Args:
            status: Task status to filter by
            
        Returns:
            List of tasks with given status
        """
        async with self.lock:
            return [task for task in self.tasks.values() if task.status == status]
    
    async def get_task_summary(self) -> TaskSummary:
        """
        Get summary of all tasks
        
        Returns:
            Task summary statistics
        """
        async with self.lock:
            total = len(self.tasks)
            queued = sum(1 for t in self.tasks.values() if t.status == TaskStatus.QUEUED)
            running = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING)
            completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
            failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
            
            return TaskSummary(
                total_tasks=total,
                queued_tasks=queued,
                running_tasks=running,
                completed_tasks=completed,
                failed_tasks=failed
            )
    
    async def clear_completed_tasks(self):
        """Clear all completed tasks"""
        async with self.lock:
            to_remove = [tid for tid, task in self.tasks.items() 
                        if task.status == TaskStatus.COMPLETED]
            for tid in to_remove:
                del self.tasks[tid]
            logger.info(f"Cleared {len(to_remove)} completed tasks")
    
    async def shutdown(self):
        """Shutdown the repository"""
        self._shutdown = True
        logger.info("Task repository shutting down")
        
        # Log final summary
        summary = await self.get_task_summary()
        logger.info(f"Final task summary: {summary.dict()}")


# Global task repository instance
task_repository = TaskRepository()
