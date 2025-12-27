"""Cloud URLs scanner - detects cloud provider URLs"""
from typing import List
import logging

from app.scanners.base import BaseScanner
from app.models.schemas import Finding, SeverityLevel, ConfidenceLevel
from app.utils.constants import CLOUD_URLS_REGEX


logger = logging.getLogger(__name__)


class CloudURLsScanner(BaseScanner):
    """Scanner for detecting cloud provider URLs"""
    
    async def scan(self) -> List[Finding]:
        """
        Scan for cloud URLs
        
        Returns:
            List of findings
        """
        findings = []
        matches = []
        
        # Find all cloud URL matches
        for match in CLOUD_URLS_REGEX.finditer(self.content):
            matches.append(match.group())
        
        # Create finding if matches found
        if matches:
            # Remove duplicates while preserving order
            unique_matches = list(dict.fromkeys(matches))
            findings.append(
                self.create_finding(
                    title="[JS Miner] Cloud Resources",
                    description="The following cloud URLs were found in a static file. "
                               "Supported cloud providers: AWS, Azure, Google Cloud, CloudFront, "
                               "DigitalOcean, Oracle, Alibaba, Firebase, Rackspace, DreamHost.",
                    matches=unique_matches,
                    severity=SeverityLevel.INFORMATION,
                    confidence=ConfidenceLevel.CERTAIN
                )
            )
        
        return findings
