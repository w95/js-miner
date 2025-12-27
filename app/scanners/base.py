"""Base scanner class"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
import logging
import httpx

from app.models.schemas import Finding, SeverityLevel, ConfidenceLevel
from app.core.task_repository import task_repository


logger = logging.getLogger(__name__)


class BaseScanner(ABC):
    """Base class for all scanners"""
    
    def __init__(self, url: str, content: str, task_id: UUID):
        """
        Initialize scanner
        
        Args:
            url: URL being scanned
            content: Content to scan
            task_id: Task UUID
        """
        self.url = url
        self.content = content
        self.task_id = task_id
        self.findings: List[Finding] = []
    
    @abstractmethod
    async def scan(self) -> List[Finding]:
        """
        Perform the scan
        
        Returns:
            List of findings
        """
        pass
    
    def create_finding(
        self,
        title: str,
        description: str,
        matches: List[str],
        severity: SeverityLevel,
        confidence: ConfidenceLevel
    ) -> Finding:
        """
        Create a finding object
        
        Args:
            title: Finding title
            description: Finding description
            matches: List of matched strings
            severity: Severity level
            confidence: Confidence level
            
        Returns:
            Finding object
        """
        return Finding(
            title=title,
            description=description,
            severity=severity,
            confidence=confidence,
            matches=matches,
            match_count=len(matches),
            url=self.url
        )
    
    async def run(self) -> List[Finding]:
        """
        Run the scanner with task tracking
        
        Returns:
            List of findings
        """
        try:
            await task_repository.start_task(self.task_id)
            logger.info(f"Running {self.__class__.__name__} on {self.url}")
            
            findings = await self.scan()
            
            await task_repository.complete_task(self.task_id)
            logger.info(f"Completed {self.__class__.__name__} on {self.url} - Found {len(findings)} issues")
            
            return findings
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__} on {self.url}: {str(e)}", exc_info=True)
            await task_repository.fail_task(self.task_id)
            raise


async def fetch_url_content(url: str, headers: Optional[dict] = None) -> Optional[str]:
    """
    Fetch content from URL
    
    Args:
        url: URL to fetch
        headers: Optional HTTP headers
        
    Returns:
        Content string or None
    """
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers or {})
            response.raise_for_status()
            return response.text
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        return None
