"""Dependency confusion scanner - detects vulnerable NPM packages"""
from typing import List, Set
import logging
import httpx

from app.scanners.base import BaseScanner
from app.models.schemas import Finding, SeverityLevel, ConfidenceLevel
from app.utils.constants import EXTRACT_DEPENDENCIES_REGEX, EXTRACT_FROM_NODE_MODULES
from app.utils.helpers import NPMPackage
from app.config import settings


logger = logging.getLogger(__name__)


class DependencyConfusionScanner(BaseScanner):
    """Scanner for detecting dependency confusion vulnerabilities"""
    
    def __init__(self, url: str, content: str, task_id, find_with_regex: bool = True):
        """
        Initialize scanner
        
        Args:
            url: URL being scanned
            content: Content to scan
            task_id: Task UUID
            find_with_regex: If True, use regex to find dependencies
        """
        super().__init__(url, content, task_id)
        self.find_with_regex = find_with_regex
    
    async def scan(self) -> List[Finding]:
        """
        Scan for dependency confusion vulnerabilities
        
        Returns:
            List of findings
        """
        findings = []
        unique_packages: Set[NPMPackage] = set()
        all_matches = []
        
        # Approach 1: Extract dependencies using regex
        if self.find_with_regex:
            # Remove whitespace for better matching
            cleaned_content = self.content.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
            
            for match in EXTRACT_DEPENDENCIES_REGEX.finditer(cleaned_content):
                try:
                    # Group 2 should contain the dependencies list
                    if len(match.groups()) >= 2:
                        dependency_list = match.group(2)
                        dependencies = dependency_list.split(",")
                        
                        for dependency in dependencies:
                            npm_package = NPMPackage(dependency)
                            if npm_package.is_name_valid():
                                unique_packages.add(npm_package)
                                all_matches.append(npm_package.get_name_with_version())
                except Exception as e:
                    logger.debug(f"Error processing dependency match: {str(e)}")
                    continue
        
        # Approach 2: Extract from node_modules paths
        for match in EXTRACT_FROM_NODE_MODULES.finditer(self.content):
            try:
                package_name = match.group(1)
                npm_package = NPMPackage(package_name, disclosed_name_only=True)
                if npm_package.is_name_valid():
                    unique_packages.add(npm_package)
                    all_matches.append(npm_package.get_name_with_version())
            except Exception as e:
                logger.debug(f"Error processing node_modules match: {str(e)}")
                continue
        
        # Report all found dependencies as informational
        if all_matches:
            unique_matches = list(dict.fromkeys(all_matches))
            findings.append(
                self.create_finding(
                    title="[JS Miner] Dependencies",
                    description="The following dependencies were found in a static file.",
                    matches=unique_matches,
                    severity=SeverityLevel.INFORMATION,
                    confidence=ConfidenceLevel.CERTAIN
                )
            )
        
        # Verify each package for dependency confusion
        if unique_packages:
            # Check connection to NPM registry
            if not await self._is_npm_connection_ok():
                logger.warning("Cannot connect to NPM registry - skipping dependency confusion checks")
                return findings
            
            # Check each package
            for npm_package in unique_packages:
                package_findings = await self._verify_package(npm_package)
                findings.extend(package_findings)
        
        return findings
    
    async def _is_npm_connection_ok(self) -> bool:
        """
        Check if NPM registry is accessible
        
        Returns:
            True if connection is OK
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Test both NPM website and registry
                npm_response = await client.get(f"{settings.NPM_JS_URL}/robots.txt")
                registry_response = await client.get(settings.NPM_REGISTRY_URL)
                
                return npm_response.status_code == 200 and registry_response.status_code == 200
        except Exception as e:
            logger.error(f"Error connecting to NPM: {str(e)}")
            return False
    
    async def _verify_package(self, npm_package: NPMPackage) -> List[Finding]:
        """
        Verify if package is vulnerable to dependency confusion
        
        Args:
            npm_package: NPM package to verify
            
        Returns:
            List of findings
        """
        findings = []
        
        try:
            # Check if version is valid NPM semantic versioning
            if not npm_package.is_version_valid_npm():
                findings.append(
                    self.create_finding(
                        title="[JS Miner] Dependency (Non-NPM registry package)",
                        description="The following non-NPM dependency was found in a static file. "
                                  "The version might contain a public repository URL, a private repository URL "
                                  "or a file path. Manual review is advised.",
                        matches=[npm_package.get_name_with_version()],
                        severity=SeverityLevel.INFORMATION,
                        confidence=ConfidenceLevel.CERTAIN
                    )
                )
                return findings
            
            # Check for scoped packages
            if npm_package.name.startswith("@"):
                org_name = npm_package.get_org_name_from_scoped_dependency()
                if org_name:
                    org_url = f"{settings.NPM_JS_URL}/org/{org_name}"
                    
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        response = await client.get(org_url)
                        
                        if response.status_code == 404:
                            # Organization doesn't exist - potential vulnerability
                            findings.append(
                                self.create_finding(
                                    title="[JS Miner] Dependency (organization not found)",
                                    description=f"The following potentially exploitable dependency was found in a static file. "
                                              f"The organization does not seem to be available, which indicates that it can be "
                                              f"registered: {org_url}",
                                    matches=[npm_package.get_name_with_version()],
                                    severity=SeverityLevel.HIGH,
                                    confidence=ConfidenceLevel.CERTAIN
                                )
                            )
            else:
                # Check public NPM package
                package_url = f"{settings.NPM_REGISTRY_URL}/{npm_package.name}"
                
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(package_url)
                    
                    if response.status_code == 404:
                        # Package doesn't exist - potential vulnerability
                        findings.append(
                            self.create_finding(
                                title="[JS Miner] Dependency Confusion",
                                description=f"The following potentially exploitable dependency was found in a static file. "
                                          f"There was no entry for this package on the 'npm js' registry: {package_url}",
                                matches=[npm_package.get_name_with_version()],
                                severity=SeverityLevel.HIGH,
                                confidence=ConfidenceLevel.CERTAIN
                            )
                        )
        except Exception as e:
            logger.error(f"Error verifying package {npm_package}: {str(e)}")
        
        return findings
