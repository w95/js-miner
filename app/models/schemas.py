"""Pydantic models for request/response schemas"""
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID


class TaskStatus(str, Enum):
    """Task status enumeration"""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskName(str, Enum):
    """Task name enumeration"""
    SECRETS_SCAN = "secrets_scan"
    SUBDOMAINS_SCAN = "subdomains_scan"
    CLOUD_URLS_SCAN = "cloud_urls_scan"
    DEPENDENCY_CONFUSION_SCAN = "dependency_confusion_scan"
    ENDPOINTS_FINDER = "endpoints_finder"
    INLINE_JS_SOURCE_MAPPER = "inline_js_source_mapper"
    SOURCE_MAPPER_ACTIVE_SCAN = "source_mapper_active_scan"
    STATIC_FILES_DUMPER = "static_files_dumper"


class ScanType(str, Enum):
    """Scan type enumeration"""
    SECRETS = "secrets"
    SUBDOMAINS = "subdomains"
    CLOUD_URLS = "cloud_urls"
    DEPENDENCY_CONFUSION = "dependency_confusion"
    ENDPOINTS = "endpoints"
    ALL_PASSIVE = "all_passive"
    ALL = "all"


class SeverityLevel(str, Enum):
    """Severity level enumeration"""
    INFORMATION = "Information"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class ConfidenceLevel(str, Enum):
    """Confidence level enumeration"""
    TENTATIVE = "Tentative"
    FIRM = "Firm"
    CERTAIN = "Certain"


class ScanRequest(BaseModel):
    """Request model for scanning"""
    url: HttpUrl = Field(..., description="URL to scan")
    content: Optional[str] = Field(None, description="File content to scan (optional)")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description="HTTP headers")
    scan_types: Optional[List[ScanType]] = Field(
        default=[ScanType.ALL_PASSIVE],
        description="Types of scans to run"
    )


class BatchScanRequest(BaseModel):
    """Request model for batch scanning"""
    urls: List[HttpUrl] = Field(..., description="URLs to scan")
    scan_types: Optional[List[ScanType]] = Field(
        default=[ScanType.ALL_PASSIVE],
        description="Types of scans to run"
    )


class Finding(BaseModel):
    """Individual finding from a scan"""
    title: str = Field(..., description="Finding title")
    description: str = Field(..., description="Finding description")
    severity: SeverityLevel = Field(..., description="Severity level")
    confidence: ConfidenceLevel = Field(..., description="Confidence level")
    matches: List[str] = Field(default_factory=list, description="Matched strings")
    match_count: int = Field(..., description="Number of matches")
    url: str = Field(..., description="URL where finding was discovered")


class ScanResult(BaseModel):
    """Result from a scan"""
    task_id: UUID = Field(..., description="Task ID")
    url: str = Field(..., description="Scanned URL")
    scan_type: TaskName = Field(..., description="Type of scan performed")
    status: TaskStatus = Field(..., description="Task status")
    findings: List[Finding] = Field(default_factory=list, description="List of findings")
    started_at: Optional[datetime] = Field(None, description="Task start time")
    completed_at: Optional[datetime] = Field(None, description="Task completion time")
    error: Optional[str] = Field(None, description="Error message if failed")


class TaskInfo(BaseModel):
    """Task information"""
    task_id: UUID = Field(..., description="Task ID")
    url: str = Field(..., description="Task URL")
    task_name: TaskName = Field(..., description="Task name")
    status: TaskStatus = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Creation time")
    started_at: Optional[datetime] = Field(None, description="Start time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")


class TaskSummary(BaseModel):
    """Summary of all tasks"""
    total_tasks: int = Field(..., description="Total number of tasks")
    queued_tasks: int = Field(..., description="Number of queued tasks")
    running_tasks: int = Field(..., description="Number of running tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    failed_tasks: int = Field(..., description="Number of failed tasks")


class ScanResponse(BaseModel):
    """Response after initiating a scan"""
    message: str = Field(..., description="Response message")
    task_ids: List[UUID] = Field(..., description="List of created task IDs")
    task_count: int = Field(..., description="Number of tasks created")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    tasks: TaskSummary = Field(..., description="Task summary")
