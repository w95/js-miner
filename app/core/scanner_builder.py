"""Scanner builder for managing scan operations"""
import asyncio
from typing import List, Dict, Optional
from uuid import UUID
import logging

from app.models.schemas import (
    ScanType, TaskName, Finding, ScanResult, TaskStatus
)
from app.scanners.secrets import SecretsScanner
from app.scanners.subdomains import SubDomainsScanner
from app.scanners.cloud_urls import CloudURLsScanner
from app.scanners.dependency_confusion import DependencyConfusionScanner
from app.scanners.endpoints import EndpointsScanner
from app.scanners.base import fetch_url_content
from app.core.task_repository import task_repository
from app.config import settings


logger = logging.getLogger(__name__)


class ScannerBuilder:
    """Builder for creating and running scanners"""
    
    def __init__(self, url: str, content: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        """
        Initialize scanner builder
        
        Args:
            url: URL to scan
            content: Optional content (if not provided, will fetch from URL)
            headers: Optional HTTP headers for fetching content
        """
        self.url = url
        self.content = content
        self.headers = headers or {}
        self.scan_types: List[ScanType] = []
    
    def with_scan_types(self, scan_types: List[ScanType]) -> 'ScannerBuilder':
        """
        Set scan types to run
        
        Args:
            scan_types: List of scan types
            
        Returns:
            Self for chaining
        """
        self.scan_types = scan_types
        return self
    
    async def execute(self) -> List[ScanResult]:
        """
        Execute all configured scans
        
        Returns:
            List of scan results
        """
        results = []
        
        # Fetch content if not provided
        if not self.content:
            logger.info(f"Fetching content from {self.url}")
            self.content = await fetch_url_content(self.url, self.headers)
            
            if not self.content:
                logger.error(f"Failed to fetch content from {self.url}")
                return results
        
        # Expand scan types if needed
        scan_types = self._expand_scan_types(self.scan_types)
        
        # Create tasks for each scan type
        tasks = []
        task_ids = []
        
        for scan_type in scan_types:
            task_name = self._scan_type_to_task_name(scan_type)
            task_id = await task_repository.create_task(self.url, task_name)
            task_ids.append(task_id)
            
            # Create scanner and add to tasks
            scanner = await self._create_scanner(scan_type, task_id)
            if scanner:
                tasks.append(self._run_scanner(scanner, task_id, task_name))
        
        # Run all scans concurrently
        if tasks:
            scan_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for scan_result in scan_results:
                if isinstance(scan_result, Exception):
                    logger.error(f"Scan failed with exception: {str(scan_result)}")
                elif scan_result:
                    results.append(scan_result)
        
        return results
    
    async def _create_scanner(self, scan_type: ScanType, task_id: UUID):
        """
        Create scanner instance based on scan type
        
        Args:
            scan_type: Type of scan
            task_id: Task UUID
            
        Returns:
            Scanner instance
        """
        if scan_type == ScanType.SECRETS:
            return SecretsScanner(self.url, self.content, task_id)
        elif scan_type == ScanType.SUBDOMAINS:
            return SubDomainsScanner(self.url, self.content, task_id)
        elif scan_type == ScanType.CLOUD_URLS:
            return CloudURLsScanner(self.url, self.content, task_id)
        elif scan_type == ScanType.DEPENDENCY_CONFUSION:
            return DependencyConfusionScanner(self.url, self.content, task_id, find_with_regex=True)
        elif scan_type == ScanType.ENDPOINTS:
            return EndpointsScanner(self.url, self.content, task_id)
        else:
            logger.warning(f"Unknown scan type: {scan_type}")
            return None
    
    async def _run_scanner(self, scanner, task_id: UUID, task_name: TaskName) -> ScanResult:
        """
        Run a scanner and return result
        
        Args:
            scanner: Scanner instance
            task_id: Task UUID
            task_name: Task name
            
        Returns:
            Scan result
        """
        try:
            findings = await scanner.run()
            task_info = await task_repository.get_task(task_id)
            
            return ScanResult(
                task_id=task_id,
                url=self.url,
                scan_type=task_name,
                status=TaskStatus.COMPLETED,
                findings=findings,
                started_at=task_info.started_at if task_info else None,
                completed_at=task_info.completed_at if task_info else None,
                error=None
            )
        except Exception as e:
            logger.error(f"Error running scanner: {str(e)}", exc_info=True)
            task_info = await task_repository.get_task(task_id)
            
            return ScanResult(
                task_id=task_id,
                url=self.url,
                scan_type=task_name,
                status=TaskStatus.FAILED,
                findings=[],
                started_at=task_info.started_at if task_info else None,
                completed_at=task_info.completed_at if task_info else None,
                error=str(e)
            )
    
    def _expand_scan_types(self, scan_types: List[ScanType]) -> List[ScanType]:
        """
        Expand composite scan types into individual scans
        
        Args:
            scan_types: List of scan types
            
        Returns:
            Expanded list of scan types
        """
        expanded = []
        
        for scan_type in scan_types:
            if scan_type == ScanType.ALL_PASSIVE:
                expanded.extend([
                    ScanType.SECRETS,
                    ScanType.SUBDOMAINS,
                    ScanType.CLOUD_URLS,
                    ScanType.DEPENDENCY_CONFUSION,
                    ScanType.ENDPOINTS
                ])
            elif scan_type == ScanType.ALL:
                expanded.extend([
                    ScanType.SECRETS,
                    ScanType.SUBDOMAINS,
                    ScanType.CLOUD_URLS,
                    ScanType.DEPENDENCY_CONFUSION,
                    ScanType.ENDPOINTS
                ])
            else:
                expanded.append(scan_type)
        
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for item in expanded:
            if item not in seen:
                seen.add(item)
                result.append(item)
        
        return result
    
    def _scan_type_to_task_name(self, scan_type: ScanType) -> TaskName:
        """
        Convert scan type to task name
        
        Args:
            scan_type: Scan type
            
        Returns:
            Task name
        """
        mapping = {
            ScanType.SECRETS: TaskName.SECRETS_SCAN,
            ScanType.SUBDOMAINS: TaskName.SUBDOMAINS_SCAN,
            ScanType.CLOUD_URLS: TaskName.CLOUD_URLS_SCAN,
            ScanType.DEPENDENCY_CONFUSION: TaskName.DEPENDENCY_CONFUSION_SCAN,
            ScanType.ENDPOINTS: TaskName.ENDPOINTS_FINDER,
        }
        return mapping.get(scan_type, TaskName.SECRETS_SCAN)
