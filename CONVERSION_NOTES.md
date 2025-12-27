# Burp JS Miner to FastAPI Conversion Notes

## Conversion Overview

This document outlines the conversion process from the Burp Suite Java extension to a FastAPI Python application.

## Architecture Changes

### From Burp Suite Extension to FastAPI

| Component | Original (Java) | Converted (Python/FastAPI) |
|-----------|----------------|----------------------------|
| Main Entry | `BurpExtender.java` | `app/main.py` |
| Configuration | Burp settings API | Environment variables + Pydantic |
| Execution Model | Thread pool (ExecutorService) | Async/await with asyncio |
| Task Management | Custom TaskRepository | Enhanced async TaskRepository |
| HTTP Client | Burp callbacks | httpx async client |
| Regex Engine | Google RE2J | Python regex library |
| Menu System | Swing JMenu | REST API endpoints |

## Key Conversions

### 1. BurpExtender → FastAPI Application

**Original:**
```java
public class BurpExtender implements IBurpExtender, IContextMenuFactory {
    @Override
    public void registerExtenderCallbacks(IBurpExtenderCallbacks callbacks) {
        // Initialize extension
    }
}
```

**Converted:**
```python
from fastapi import FastAPI

app = FastAPI(
    title="JS Miner API",
    version="2.0.0"
)

@app.get("/")
async def root():
    return {"status": "running"}
```

### 2. Scanner Implementations

**Original (Java):**
```java
public class Secrets implements Runnable {
    public void run() {
        Matcher matcher = SECRETS_REGEX.matcher(content);
        while (matcher.find()) {
            // Process matches
        }
    }
}
```

**Converted (Python):**
```python
class SecretsScanner(BaseScanner):
    async def scan(self) -> List[Finding]:
        for match in SECRETS_REGEX.finditer(self.content):
            # Process matches
        return findings
```

### 3. Menu Items → REST Endpoints

**Original (Java - Right-click menu):**
```java
JMenuItem secretsMenuItem = new JMenuItem("Secrets");
secretsMenuItem.addActionListener(secretsItemAction);
```

**Converted (Python - REST API):**
```python
@router.post("/scans/")
async def create_scan(request: ScanRequest):
    builder = ScannerBuilder(url, content).with_scan_types(scan_types)
    return await builder.execute()
```

### 4. Task Repository

**Original (Java):**
```java
public class TaskRepository {
    private final Map<UUID, Task> tasks = new ConcurrentHashMap<>();
    
    public void addTask(Task task) {
        tasks.put(task.getUuid(), task);
    }
}
```

**Converted (Python):**
```python
class TaskRepository:
    def __init__(self):
        self.tasks: Dict[UUID, TaskInfo] = {}
        self.lock = asyncio.Lock()
    
    async def create_task(self, url: str, task_name: TaskName) -> UUID:
        async with self.lock:
            self.tasks[task_id] = task_info
        return task_id
```

### 5. Scanner Builder Pattern

**Original (Java):**
```java
ScannerBuilder scannerBuilder = new ScannerBuilder.Builder(httpReqResArray)
    .scanSecrets()
    .scanSubDomains()
    .taskId(taskId)
    .build();
scannerBuilder.runScans();
```

**Converted (Python):**
```python
builder = ScannerBuilder(url, content) \
    .with_scan_types([ScanType.SECRETS, ScanType.SUBDOMAINS])

results = await builder.execute()
```

## Feature Mapping

### Scanners

| Scanner | Java Class | Python Module | Status |
|---------|-----------|---------------|--------|
| Secrets | `Secrets.java` | `scanners/secrets.py` | ✅ Complete |
| SubDomains | `SubDomains.java` | `scanners/subdomains.py` | ✅ Complete |
| Cloud URLs | `CloudURLs.java` | `scanners/cloud_urls.py` | ✅ Complete |
| Dependency Confusion | `DependencyConfusion.java` | `scanners/dependency_confusion.py` | ✅ Complete |
| Endpoints | `Endpoints.java` | `scanners/endpoints.py` | ✅ Complete |
| Active Source Mapper | `ActiveSourceMapper.java` | ⚠️ Not implemented (requires active scanning) |
| Inline Source Maps | `InlineSourceMapFiles.java` | ⚠️ Not implemented (source map specific) |
| Static Files Dumper | `StaticFilesDumper.java` | ⚠️ Not implemented (file system operations) |

### Utilities

| Utility | Java Class | Python Module | Status |
|---------|-----------|---------------|--------|
| Constants | `Constants.java` | `utils/constants.py` | ✅ Complete |
| Utilities | `Utilities.java` | `utils/helpers.py` | ✅ Complete |
| NPM Package | `NPMPackage.java` | `utils/helpers.py` (NPMPackage class) | ✅ Complete |
| Custom Scan Issue | `CustomScanIssue.java` | `models/schemas.py` (Finding) | ✅ Complete |

## Technical Decisions

### 1. Async/Await vs Thread Pool

**Decision:** Use Python's asyncio instead of Java's ExecutorService
**Reasoning:**
- Better performance for I/O-bound operations (HTTP requests, file reading)
- More Pythonic and maintainable
- Native FastAPI support

### 2. REST API vs Extension Interface

**Decision:** Provide REST API endpoints instead of Burp menu items
**Reasoning:**
- Platform-independent
- Easier integration with CI/CD
- Supports programmatic access
- Can be used by any HTTP client

### 3. Pydantic for Validation

**Decision:** Use Pydantic models for request/response validation
**Reasoning:**
- Type safety
- Automatic validation
- OpenAPI schema generation
- Better developer experience

### 4. Environment Variables for Configuration

**Decision:** Use .env files and environment variables instead of Burp settings API
**Reasoning:**
- Standard practice for web applications
- Easy deployment configuration
- Docker-friendly
- No dependency on Burp Suite

## API Design

### Endpoint Structure

```
/api/v1/
├── scans/
│   ├── POST /              # Create scan (background)
│   ├── POST /immediate     # Execute scan immediately
│   └── POST /batch         # Batch scan multiple URLs
└── tasks/
    ├── GET /summary        # Get task statistics
    ├── GET /               # Get all tasks
    ├── GET /{task_id}      # Get specific task
    ├── GET /status/{status} # Get tasks by status
    └── DELETE /completed   # Clear completed tasks
```

## Dependencies Mapping

### Java Dependencies
```gradle
implementation 'net.portswigger.burp.extender:burp-extender-api:2.3'
implementation 'com.fasterxml.jackson.core:jackson-core:2.13.3'
implementation 'com.fasterxml.jackson.core:jackson-databind:2.13.3'
implementation 'com.google.re2j:re2j:1.7'
```

### Python Dependencies
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
httpx==0.26.0
regex==2023.12.25
```

## Testing Strategy

### Original (Burp Suite)
- Manual testing through Burp interface
- Right-click menu interactions
- Visual inspection of issues

### Converted (FastAPI)
- Unit tests for each scanner
- Integration tests for API endpoints
- Pytest framework
- Mock HTTP responses

## Deployment Options

### Original
- Load JAR into Burp Suite
- BApp Store distribution

### Converted
- Docker container
- Kubernetes deployment
- Traditional VPS/server
- Cloud platforms (AWS, GCP, Azure)
- Serverless (with modifications)

## Limitations & Trade-offs

### Not Converted
1. **Active Source Mapper** - Requires active HTTP requests to guess .map file locations
2. **Inline Source Maps** - Base64 source map parsing and file writing
3. **Static Files Dumper** - Bulk file system operations
4. **Burp-specific features** - Issue markers, response highlighting

### Trade-offs
- **No Burp Integration:** Standalone service instead of integrated tool
- **Manual Content Fetching:** User must provide content or API fetches it
- **Different Workflow:** API calls instead of right-click menu

## Future Enhancements

1. **Add Missing Scanners**
   - Implement source map parser
   - Add file dumping capabilities

2. **Enhanced Features**
   - WebSocket support for real-time updates
   - Database persistence for findings
   - User authentication and authorization
   - Rate limiting
   - Caching layer

3. **Integration Options**
   - Webhook notifications
   - Slack/Discord integration
   - Export to various formats (JSON, CSV, PDF)
   - Integration with other security tools

## Usage Examples Comparison

### Original (Burp Suite)
1. Navigate to target in Burp
2. Right-click on domain in Site Map
3. Select "JS Miner" → "Run all passive scans"
4. View results in Burp issues

### Converted (FastAPI)
```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/app.js",
    "scan_types": ["all_passive"]
  }'
```

## Performance Considerations

### Original (Java)
- Thread pool with configurable size
- Synchronous HTTP requests via Burp
- In-memory task tracking

### Converted (Python)
- Async I/O for better concurrency
- Connection pooling with httpx
- Non-blocking operations
- Configurable worker limits

## Conclusion

The conversion successfully maintains all core functionality while providing:
- Modern REST API interface
- Better scalability and performance
- Platform independence
- Easier integration and automation
- Improved maintainability

The FastAPI version can be used as a standalone security scanning service or integrated into larger security pipelines.
