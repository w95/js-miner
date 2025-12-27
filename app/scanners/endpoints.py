"""API endpoints scanner - detects REST API endpoints"""
from typing import List
import logging

from app.scanners.base import BaseScanner
from app.models.schemas import Finding, SeverityLevel, ConfidenceLevel
from app.utils.constants import (
    ENDPOINTS_GET_REGEX,
    ENDPOINTS_POST_REGEX,
    ENDPOINTS_PUT_REGEX,
    ENDPOINTS_DELETE_REGEX,
    ENDPOINTS_PATCH_REGEX
)


logger = logging.getLogger(__name__)


class EndpointsScanner(BaseScanner):
    """Scanner for detecting API endpoints"""
    
    async def scan(self) -> List[Finding]:
        """
        Scan for API endpoints
        
        Returns:
            List of findings
        """
        findings = []
        
        # Scan for each HTTP method
        findings.extend(await self._find_endpoints(ENDPOINTS_GET_REGEX, "GET"))
        findings.extend(await self._find_endpoints(ENDPOINTS_POST_REGEX, "POST"))
        findings.extend(await self._find_endpoints(ENDPOINTS_PUT_REGEX, "PUT"))
        findings.extend(await self._find_endpoints(ENDPOINTS_DELETE_REGEX, "DELETE"))
        findings.extend(await self._find_endpoints(ENDPOINTS_PATCH_REGEX, "PATCH"))
        
        return findings
    
    async def _find_endpoints(self, pattern, method: str) -> List[Finding]:
        """
        Find endpoints for a specific HTTP method
        
        Args:
            pattern: Regex pattern to use
            method: HTTP method name
            
        Returns:
            List of findings
        """
        findings = []
        matches = []
        
        # Find all endpoint matches
        for match in pattern.finditer(self.content):
            try:
                # Group 1 should contain the endpoint path
                if len(match.groups()) >= 1:
                    endpoint = match.group(1)
                    
                    # Validate endpoint
                    if self._is_valid_endpoint(endpoint):
                        matches.append(endpoint)
            except Exception as e:
                logger.debug(f"Error processing endpoint match: {str(e)}")
                continue
        
        # Create finding if matches found
        if matches:
            # Remove duplicates while preserving order
            unique_matches = list(dict.fromkeys(matches))
            findings.append(
                self.create_finding(
                    title=f"[JS Miner] API Endpoints ({method})",
                    description=f"The following {method} API endpoints were found in a static file.",
                    matches=unique_matches,
                    severity=SeverityLevel.INFORMATION,
                    confidence=ConfidenceLevel.CERTAIN
                )
            )
        
        return findings
    
    def _is_valid_endpoint(self, endpoint: str) -> bool:
        """
        Validate if endpoint is a valid API path
        
        Args:
            endpoint: Endpoint string to validate
            
        Returns:
            True if valid endpoint
        """
        # Must contain forward slash
        if "/" not in endpoint:
            return False
        
        # Should not contain HTML-like tags
        if "<" in endpoint or ">" in endpoint:
            return False
        
        # Should not be too short
        if len(endpoint) < 2:
            return False
        
        return True
