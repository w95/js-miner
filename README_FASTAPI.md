# JS Miner FastAPI

A modern FastAPI-based REST API for analyzing JavaScript and JSON files for security issues. This is a conversion of the original Burp Suite extension to a standalone web service.

## Overview

JS Miner API scans static files (primarily JavaScript and JSON) to identify:

- **Secrets/Credentials** - API keys, tokens, passwords using Shannon entropy analysis
- **Subdomains** - Subdomain discovery from static files
- **Cloud URLs** - AWS, Azure, Google Cloud, and other cloud provider URLs
- **Dependency Confusion** - Vulnerable NPM packages and missing dependencies
- **API Endpoints** - GET/POST/PUT/DELETE/PATCH endpoint discovery

## Features

### Converted from Burp Suite Extension

This FastAPI application is a complete conversion of the Burp Suite JS Miner extension, providing:

- ✅ All scanner functionality from the original Burp extension
- ✅ RESTful API for programmatic access
- ✅ Async/await for high performance
- ✅ Task management and tracking
- ✅ Batch scanning capabilities
- ✅ Modern Python architecture

### Security Scanners

1. **Secrets Scanner**
   - Uses Shannon entropy to improve detection accuracy
   - Supports multiple credential patterns (API keys, tokens, passwords)
   - HTTP Basic Auth detection
   - Confidence levels: High (firm) and Low (tentative)

2. **Subdomain Scanner**
   - Discovers subdomains from static files
   - Filters out common false positives

3. **Cloud URLs Scanner**
   - Supports: AWS, Azure, Google Cloud, CloudFront, DigitalOcean, Oracle, Alibaba, Firebase, Rackspace, DreamHost
   - Identifies cloud storage URLs and resources

4. **Dependency Confusion Scanner**
   - Identifies NPM packages in JavaScript files
   - Verifies packages against NPM registry
   - Detects missing packages and organizations
   - Reports potential supply chain vulnerabilities

5. **API Endpoints Scanner**
   - Finds REST API endpoints
   - Supports GET, POST, PUT, DELETE, PATCH methods

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd workspace
```

2. Install dependencies:
```bash
pip3.10 install -r requirements.txt
```

3. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

## Usage

### Starting the Server

```bash
# Development mode with auto-reload
python3.10 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main module
python3.10 -m app.main

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### Scans

**POST /api/v1/scans/** - Create a new scan
```bash
curl -X POST "http://localhost:8000/api/v1/scans/" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/app.js",
    "scan_types": ["all_passive"]
  }'
```

**POST /api/v1/scans/immediate** - Execute scan and get immediate results
```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/app.js",
    "scan_types": ["secrets", "endpoints"]
  }'
```

**POST /api/v1/scans/batch** - Scan multiple URLs
```bash
curl -X POST "http://localhost:8000/api/v1/scans/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com/app.js",
      "https://example.com/vendor.js"
    ],
    "scan_types": ["all_passive"]
  }'
```

#### Tasks

**GET /api/v1/tasks/summary** - Get task summary
```bash
curl "http://localhost:8000/api/v1/tasks/summary"
```

**GET /api/v1/tasks/** - Get all tasks
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

**GET /api/v1/tasks/{task_id}** - Get specific task
```bash
curl "http://localhost:8000/api/v1/tasks/123e4567-e89b-12d3-a456-426614174000"
```

**GET /api/v1/tasks/status/{status}** - Get tasks by status
```bash
curl "http://localhost:8000/api/v1/tasks/status/completed"
```

**DELETE /api/v1/tasks/completed** - Clear completed tasks
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/completed"
```

### Scan Types

Available scan types:
- `secrets` - Scan for secrets and credentials
- `subdomains` - Scan for subdomains
- `cloud_urls` - Scan for cloud provider URLs
- `dependency_confusion` - Scan for vulnerable dependencies
- `endpoints` - Scan for API endpoints
- `all_passive` - Run all passive scans (recommended)
- `all` - Run all available scans

## Configuration

Configure the application using environment variables or `.env` file:

```bash
# Application
APP_NAME="JS Miner API"
APP_VERSION="2.0.0"
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
VERBOSE_LOGGING=True

# Scanner
MAX_WORKERS=10
MAX_RESPONSE_HIGHLIGHTS=500
SHANNON_ENTROPY_THRESHOLD=3.5

# NPM Registry
NPM_REGISTRY_URL=https://registry.npmjs.org
NPM_JS_URL=https://www.npmjs.com
```

## Examples

### Scanning a JavaScript File

```python
import httpx

# Immediate scan with results
response = httpx.post(
    "http://localhost:8000/api/v1/scans/immediate",
    json={
        "url": "https://example.com/main.js",
        "scan_types": ["secrets", "endpoints"]
    }
)

results = response.json()
for scan_result in results:
    print(f"Scan: {scan_result['scan_type']}")
    print(f"Findings: {len(scan_result['findings'])}")
    for finding in scan_result['findings']:
        print(f"  - {finding['title']}: {finding['match_count']} matches")
```

### Batch Scanning

```python
import httpx

# Scan multiple URLs
response = httpx.post(
    "http://localhost:8000/api/v1/scans/batch",
    json={
        "urls": [
            "https://example.com/app.js",
            "https://example.com/vendor.js",
            "https://example.com/config.json"
        ],
        "scan_types": ["all_passive"]
    }
)

print(response.json())
```

## Architecture

### Project Structure

```
workspace/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── scans.py         # Scan endpoints
│   │   └── tasks.py         # Task endpoints
│   ├── core/                # Core business logic
│   │   ├── __init__.py
│   │   ├── scanner_builder.py  # Scanner orchestration
│   │   └── task_repository.py  # Task management
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   ├── scanners/            # Scanner implementations
│   │   ├── __init__.py
│   │   ├── base.py          # Base scanner class
│   │   ├── secrets.py       # Secrets scanner
│   │   ├── subdomains.py    # Subdomains scanner
│   │   ├── cloud_urls.py    # Cloud URLs scanner
│   │   ├── dependency_confusion.py  # Dependency scanner
│   │   └── endpoints.py     # Endpoints scanner
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── constants.py     # Constants and regex patterns
│       └── helpers.py       # Helper functions
├── requirements.txt
├── .env.example
└── README_FASTAPI.md
```

### Design Patterns

- **Builder Pattern**: `ScannerBuilder` for flexible scan configuration
- **Repository Pattern**: `TaskRepository` for task management
- **Factory Pattern**: Scanner creation based on scan types
- **Async/Await**: Concurrent scanning for high performance

## Comparison with Original Burp Extension

| Feature | Burp Extension | FastAPI API |
|---------|---------------|-------------|
| Secrets Detection | ✅ | ✅ |
| Subdomain Discovery | ✅ | ✅ |
| Cloud URLs | ✅ | ✅ |
| Dependency Confusion | ✅ | ✅ |
| API Endpoints | ✅ | ✅ |
| Platform | Burp Suite only | Standalone |
| API Access | ❌ | ✅ |
| Batch Processing | Limited | ✅ |
| Task Management | Basic | Advanced |
| Concurrent Scans | Thread pool | Async/await |
| Integration | Burp only | Any HTTP client |

## Limitations & Notes

- Like the original tool, this may produce false positives
- Manual review of findings is recommended
- For best results, scan complete JavaScript files (not minified stubs)
- Dependency confusion checks require internet access to NPM registry

## License

This project is licensed under the terms of the Apache 2.0 open source license.

## Original Project

Converted from: [burp-JS-Miner](https://github.com/minamo7sen/burp-JS-Miner)
Original Author: Mina M. Edwar

## Disclaimer

It is the user's responsibility to obey all applicable local, state and federal laws. The author assumes no liability and is not responsible for any misuse or damage caused by this tool.
