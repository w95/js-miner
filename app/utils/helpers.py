"""Helper utility functions"""
import base64
import hashlib
import math
import regex as re
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, urljoin
from collections import Counter


def calculate_shannon_entropy(text: str) -> float:
    """
    Calculate Shannon entropy of a string
    Higher entropy indicates more randomness (potentially a secret)
    
    Args:
        text: String to calculate entropy for
        
    Returns:
        Shannon entropy value
    """
    if not text:
        return 0.0
    
    # Count character frequencies
    counter = Counter(text)
    length = len(text)
    
    # Calculate entropy
    entropy = 0.0
    for count in counter.values():
        probability = count / length
        if probability > 0:
            entropy += probability * math.log2(probability)
    
    return -entropy


def is_high_entropy(text: str, threshold: float = 3.5) -> bool:
    """
    Check if text has high entropy
    
    Args:
        text: String to check
        threshold: Entropy threshold (default 3.5)
        
    Returns:
        True if entropy is above threshold
    """
    return calculate_shannon_entropy(text) >= threshold


def is_valid_base64(text: str) -> bool:
    """
    Check if text is valid base64
    
    Args:
        text: String to check
        
    Returns:
        True if valid base64
    """
    try:
        base64.b64decode(text, validate=True)
        return True
    except Exception:
        return False


def decode_base64(text: str) -> Optional[str]:
    """
    Decode base64 string
    
    Args:
        text: Base64 encoded string
        
    Returns:
        Decoded string or None if invalid
    """
    try:
        decoded_bytes = base64.b64decode(text.strip())
        return decoded_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return None


def get_root_domain(domain: str) -> Optional[str]:
    """
    Extract root domain from a full domain
    Example: sub.example.com -> example.com
    
    Args:
        domain: Full domain name
        
    Returns:
        Root domain or None
    """
    pattern = re.compile(r'[a-z0-9]+\.[a-z0-9]+$', re.IGNORECASE)
    match = pattern.search(domain)
    if match:
        return match.group()
    return None


def normalize_url(url: str) -> str:
    """
    Normalize URL by removing query strings and fragments
    
    Args:
        url: URL to normalize
        
    Returns:
        Normalized URL
    """
    parsed = urlparse(url)
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return normalized


def extract_domain_from_url(url: str) -> Optional[str]:
    """
    Extract domain from URL
    
    Args:
        url: URL string
        
    Returns:
        Domain or None
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def is_matched_domain_valid(matched_domain: str, root_domain: str, request_domain: str) -> bool:
    """
    Validate if matched subdomain is valid and not redundant
    
    Args:
        matched_domain: Found subdomain
        root_domain: Root domain
        request_domain: Original request domain
        
    Returns:
        True if valid subdomain
    """
    if not matched_domain.endswith(root_domain):
        return False
    
    # Exclude common patterns
    if matched_domain in [f"www.{request_domain}", request_domain, f"www.{root_domain}"]:
        return False
    
    return True


def calculate_hash(data: bytes) -> str:
    """
    Calculate SHA256 hash of data
    
    Args:
        data: Bytes to hash
        
    Returns:
        Hex digest of hash
    """
    return hashlib.sha256(data).hexdigest()


def is_static_file(url: str, extensions: List[str]) -> bool:
    """
    Check if URL points to a static file with given extensions
    
    Args:
        url: URL to check
        extensions: List of file extensions (e.g., ['.js', '.json'])
        
    Returns:
        True if URL matches any extension
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    return any(path.endswith(ext) for ext in extensions)


def is_not_false_positive_secret(secret: str) -> bool:
    """
    Check if secret is not a common false positive
    
    Args:
        secret: Secret string to check
        
    Returns:
        True if not a false positive
    """
    # Cleanup the secret
    secret_clean = secret.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "").replace("*", "")
    
    # Minimum length check
    if len(secret_clean) <= 4:
        return False
    
    # Check against known false positives
    false_positives = ["basic", "bearer", "token"]
    if secret_clean.lower() in false_positives:
        return False
    
    return True


def format_finding_html(matches: List[str]) -> str:
    """
    Format list of matches as HTML list
    
    Args:
        matches: List of matched strings
        
    Returns:
        HTML formatted string
    """
    if not matches:
        return ""
    
    from app.utils.constants import HTML_LIST_OPEN, HTML_LIST_BULLET_OPEN, HTML_LIST_BULLET_CLOSED, HTML_LIST_CLOSED
    
    unique_matches = list(set(matches))
    items = [f"{HTML_LIST_BULLET_OPEN}{match}{HTML_LIST_BULLET_CLOSED}" for match in unique_matches]
    return f"{HTML_LIST_OPEN}{''.join(items)}{HTML_LIST_CLOSED}"


def extract_referer_domain(headers: Dict[str, str]) -> Optional[str]:
    """
    Extract domain from Referer header
    
    Args:
        headers: HTTP headers dictionary
        
    Returns:
        Domain from referer or None
    """
    referer = headers.get("referer") or headers.get("Referer")
    if referer:
        domain = extract_domain_from_url(referer)
        if domain:
            return get_root_domain(domain)
    return None


class NPMPackage:
    """NPM Package representation"""
    
    def __init__(self, dependency_string: str, disclosed_name_only: bool = False):
        """
        Initialize NPM package from dependency string
        
        Args:
            dependency_string: Dependency string (e.g., "package:version" or "@org/package:version")
            disclosed_name_only: If True, version is not expected
        """
        self.name = ""
        self.version = ""
        self.disclosed_name_only = disclosed_name_only
        
        if disclosed_name_only:
            self.name = dependency_string.strip()
        else:
            parts = dependency_string.split(":")
            if len(parts) >= 2:
                self.name = parts[0].strip().strip('"').strip("'")
                self.version = parts[1].strip().strip('"').strip("'")
            else:
                self.name = dependency_string.strip().strip('"').strip("'")
    
    def is_name_valid(self) -> bool:
        """Check if package name is valid NPM package name"""
        if not self.name or len(self.name) < 2:
            return False
        
        # NPM package name validation
        # Can start with @ for scoped packages
        pattern = re.compile(r'^(@[a-z0-9-~][a-z0-9-._~]*/)?[a-z0-9-~][a-z0-9-._~]*$', re.IGNORECASE)
        return bool(pattern.match(self.name))
    
    def is_version_valid_npm(self) -> bool:
        """Check if version follows NPM semantic versioning"""
        if not self.version or self.disclosed_name_only:
            return True
        
        # Check for semantic versioning pattern (e.g., 1.0.0, ^1.0.0, ~1.0.0)
        pattern = re.compile(r'^[\^~]?\d+\.\d+\.\d+')
        return bool(pattern.match(self.version))
    
    def get_org_name_from_scoped_dependency(self) -> Optional[str]:
        """Extract organization name from scoped package (e.g., @org/package -> org)"""
        if self.name.startswith("@"):
            parts = self.name.split("/")
            if len(parts) >= 1:
                return parts[0][1:]  # Remove @ symbol
        return None
    
    def get_name_with_version(self) -> str:
        """Get formatted name with version"""
        if self.version and not self.disclosed_name_only:
            return f"{self.name}:{self.version}"
        return self.name
    
    def __hash__(self):
        return hash((self.name, self.version))
    
    def __eq__(self, other):
        if isinstance(other, NPMPackage):
            return self.name == other.name and self.version == other.version
        return False
    
    def __str__(self):
        return self.get_name_with_version()
