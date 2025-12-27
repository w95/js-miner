"""Subdomain scanner - detects subdomains"""
from typing import List
import regex as re
import logging
from urllib.parse import urlparse

from app.scanners.base import BaseScanner
from app.models.schemas import Finding, SeverityLevel, ConfidenceLevel
from app.utils.helpers import get_root_domain, is_matched_domain_valid


logger = logging.getLogger(__name__)


class SubDomainsScanner(BaseScanner):
    """Scanner for detecting subdomains"""
    
    async def scan(self) -> List[Finding]:
        """
        Scan for subdomains
        
        Returns:
            List of findings
        """
        findings = []
        matches = []
        
        # Parse URL to get domain
        parsed_url = urlparse(self.url)
        request_domain = parsed_url.netloc
        root_domain = get_root_domain(request_domain)
        
        if not root_domain:
            logger.warning(f"Could not extract root domain from {self.url}")
            return findings
        
        # Create regex pattern for finding subdomains
        # Pattern: ([a-z-0-9]+[.])+ followed by root domain
        subdomain_pattern = re.compile(
            rf"([a-z0-9\-]+\.)+{re.escape(root_domain)}",
            re.IGNORECASE
        )
        
        # Find all subdomain matches
        for match in subdomain_pattern.finditer(self.content):
            matched_domain = match.group()
            
            # Validate the matched domain
            if is_matched_domain_valid(matched_domain, root_domain, request_domain):
                matches.append(matched_domain)
        
        # Create finding if matches found
        if matches:
            # Remove duplicates while preserving order
            unique_matches = list(dict.fromkeys(matches))
            findings.append(
                self.create_finding(
                    title="[JS Miner] Subdomains",
                    description="The following subdomains were found in a static file.",
                    matches=unique_matches,
                    severity=SeverityLevel.INFORMATION,
                    confidence=ConfidenceLevel.CERTAIN
                )
            )
        
        return findings
