"""Constants used throughout the application"""
import regex as re

# Scan issue severities
SEVERITY_INFORMATION = "Information"
SEVERITY_LOW = "Low"
SEVERITY_MEDIUM = "Medium"
SEVERITY_HIGH = "High"
SEVERITY_CRITICAL = "Critical"

# Confidence levels
CONFIDENCE_CERTAIN = "Certain"
CONFIDENCE_FIRM = "Firm"
CONFIDENCE_TENTATIVE = "Tentative"

# Regex patterns
WHITE_SPACES = r"(\s*)"
REGEX_QUOTES = r"['\"`]"

# Cloud URLs Regex - matches various cloud provider URLs
CLOUD_URLS_REGEX = re.compile(
    r"([\w]+[.]){1,10}" +  # get up to 10 subdomain levels
    r"(s3\.amazonaws\.com|rds\.amazonaws\.com|cache\.amazonaws\.com|" +  # AWS
    r"blob\.core\.windows\.net|onedrive\.live\.com|1drv\.com|" +  # Azure
    r"storage\.googleapis\.com|storage\.cloud\.google\.com|storage-download\.googleapis\.com|" +
    r"content-storage-upload\.googleapis\.com|content-storage-download\.googleapis\.com|" +  # Google
    r"cloudfront\.net|" +
    r"digitaloceanspaces\.com|" +
    r"oraclecloud\.com|" +
    r"aliyuncs\.com|" +  # Alibaba
    r"firebaseio\.com|" +  # Firebase
    r"rackcdn\.com|" +
    r"objects\.cdn\.dream\.io|objects-us-west-1\.dream\.io)",
    re.IGNORECASE | re.MULTILINE
)

# Secrets Regex - inspired by SubDomainizer
SECRETS_REGEX = re.compile(
    r"['\"`]?(\w*)" +  # Starts with a quote then a word / white spaces
    WHITE_SPACES +
    r"(secret|token|password|passwd|authorization|bearer|aws_access_key_id|aws_secret_access_key|irc_pass|SLACK_BOT_TOKEN|id_dsa|" +
    r"secret[_-]?(key|token|secret)|" +
    r"api[_-]?(key|token|secret)|" +
    r"access[_-]?(key|token|secret)|" +
    r"auth[_-]?(key|token|secret)|" +
    r"session[_-]?(key|token|secret)|" +
    r"consumer[_-]?(key|token|secret)|" +
    r"public[_-]?(key|token|secret)|" +
    r"client[_-]?(id|token|key)|" +
    r"ssh[_-]?key|" +
    r"encrypt[_-]?(secret|key)|" +
    r"decrypt[_-]?(secret|key)|" +
    r"github[_-]?(key|token|secret)|" +
    r"slack[_-]?token)" +
    r"(\w*)" +  # in case there are any characters / white spaces
    WHITE_SPACES +
    r"['\"`]?" +  # closing quote for variable name
    WHITE_SPACES +  # white spaces
    r"[:=]+[:=>]?" +  # assignments operation
    WHITE_SPACES +
    REGEX_QUOTES +  # opening quote for secret
    WHITE_SPACES +
    r"([\w\-/~!@#$%^&*+]+)" +  # Assuming secrets will be alphanumeric with some special characters
    WHITE_SPACES +
    REGEX_QUOTES,  # closing quote for secrets
    re.IGNORECASE | re.MULTILINE
)

# HTTP Basic Auth Secrets
HTTP_BASIC_AUTH_SECRETS = re.compile(
    r"Authorization.{0,5}Basic(\s*)([A-Za-z0-9+/=]+)",
    re.MULTILINE
)

# Base64 Source Map Regex
B64_SOURCE_MAP_REGEX = re.compile(
    r"sourceMappingURL=data(.*)json(.*)base64,((?:[a-z0-9+/]{4})*(?:[a-z0-9+/]{2}==|[a-z0-9+/]{3}=)?)(\\\n)?",
    re.IGNORECASE | re.MULTILINE
)

# Extract Dependencies Regex
EXTRACT_DEPENDENCIES_REGEX = re.compile(
    r"dependencies" +  # we don't care about prefix
    r"([a-z-_0-9])*" +  # some suffix may be (e.g.: dependenciesDev1_2-3)
    REGEX_QUOTES +  # closing quote
    r":" +  # mandatory colon
    r"\{" +  # mandatory opening curly brackets
    r"(.*?)" +  # our dependencies list -> group(2)
    r"}",  # mandatory closing curly brackets
    re.IGNORECASE | re.MULTILINE
)

# Extract from node_modules
EXTRACT_FROM_NODE_MODULES = re.compile(
    r"/node_modules/(@?[a-z\-_.0-9]+)/"
)

# API Endpoints Regex
ENDPOINTS_GET_REGEX = re.compile(
    r"\.[\$]?get\(['\"`]?(.*?)['\"`]?\)",
    re.IGNORECASE | re.MULTILINE
)

ENDPOINTS_POST_REGEX = re.compile(
    r"\.[\$]?post\(['\"`]?(.*?)['\"`]?\)",
    re.IGNORECASE | re.MULTILINE
)

ENDPOINTS_PUT_REGEX = re.compile(
    r"\.[\$]?put\(['\"`]?(.*?)['\"`]?\)",
    re.IGNORECASE | re.MULTILINE
)

ENDPOINTS_DELETE_REGEX = re.compile(
    r"\.[\$]?delete\(['\"`]?(.*?)['\"`]?\)",
    re.IGNORECASE | re.MULTILINE
)

ENDPOINTS_PATCH_REGEX = re.compile(
    r"\.[\$]?patch\(['\"`]?(.*?)['\"`]?\)",
    re.IGNORECASE | re.MULTILINE
)

# File extensions
EXTENSION_JS = [".js"]
EXTENSION_JSON = [".json"]
EXTENSION_JS_JSON = [".js", ".json"]
EXTENSION_CSS = [".css"]
EXTENSION_JS_JSON_CSS_MAP = [".js", ".json", ".css", ".map"]

# HTML formatting
HTML_LIST_OPEN = "<ul>"
HTML_LIST_BULLET_OPEN = "<li> "
HTML_LIST_BULLET_CLOSED = "</li>"
HTML_LIST_CLOSED = "</ul>"
