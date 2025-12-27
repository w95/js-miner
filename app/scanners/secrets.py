"""Secrets scanner - detects credentials and API keys"""
from typing import List
import logging

from app.scanners.base import BaseScanner
from app.models.schemas import Finding, SeverityLevel, ConfidenceLevel
from app.utils.constants import SECRETS_REGEX, HTTP_BASIC_AUTH_SECRETS
from app.utils.helpers import (
    is_high_entropy,
    is_not_false_positive_secret,
    is_valid_base64,
    decode_base64
)
from app.config import settings


logger = logging.getLogger(__name__)


class SecretsScanner(BaseScanner):
    """Scanner for detecting secrets and credentials"""
    
    async def scan(self) -> List[Finding]:
        """
        Scan for secrets and credentials
        
        Returns:
            List of findings
        """
        findings = []
        
        # High confidence matches (high entropy)
        high_confidence_matches = []
        # Low confidence matches (low entropy)
        low_confidence_matches = []
        
        # Scan for general secrets
        for match in SECRETS_REGEX.finditer(self.content):
            try:
                # Group 20 should contain the actual secret value
                secret_value = match.group(20) if len(match.groups()) >= 20 else match.group()
                
                if is_high_entropy(secret_value, settings.SHANNON_ENTROPY_THRESHOLD):
                    # High entropy = high confidence
                    high_confidence_matches.append(match.group())
                else:
                    # Low entropy = low confidence, but check for false positives
                    if is_not_false_positive_secret(secret_value):
                        low_confidence_matches.append(match.group())
            except Exception as e:
                logger.debug(f"Error processing secret match: {str(e)}")
                continue
        
        # Scan for HTTP Basic Auth secrets
        for match in HTTP_BASIC_AUTH_SECRETS.finditer(self.content):
            try:
                # Group 2 should contain the base64 encoded credentials
                base64_string = match.group(2) if len(match.groups()) >= 2 else match.group()
                
                if is_valid_base64(base64_string):
                    decoded = decode_base64(base64_string)
                    if decoded and is_high_entropy(decoded, settings.SHANNON_ENTROPY_THRESHOLD):
                        high_confidence_matches.append(match.group())
                    else:
                        low_confidence_matches.append(match.group())
                else:
                    low_confidence_matches.append(match.group())
            except Exception as e:
                logger.debug(f"Error processing basic auth match: {str(e)}")
                continue
        
        # Create findings
        if high_confidence_matches:
            # Remove duplicates while preserving order
            unique_high = list(dict.fromkeys(high_confidence_matches))
            findings.append(
                self.create_finding(
                    title="[JS Miner] Secrets / Credentials",
                    description="The following secrets (with High entropy) were found in a static file.",
                    matches=unique_high,
                    severity=SeverityLevel.MEDIUM,
                    confidence=ConfidenceLevel.FIRM
                )
            )
        
        if low_confidence_matches:
            # Remove duplicates while preserving order
            unique_low = list(dict.fromkeys(low_confidence_matches))
            findings.append(
                self.create_finding(
                    title="[JS Miner] Secrets / Credentials",
                    description="The following secrets (with Low entropy) were found in a static file.",
                    matches=unique_low,
                    severity=SeverityLevel.MEDIUM,
                    confidence=ConfidenceLevel.TENTATIVE
                )
            )
        
        return findings
