# JS Miner FastAPI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
# Using pip
pip3.10 install -r requirements.txt

# Or using the run script
chmod +x run.sh
./run.sh
```

### 2. Start the Server

```bash
# Development mode (auto-reload)
python3.10 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the run script
./run.sh
```

### 3. Access the API

- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

### 4. Try Your First Scan

#### Option A: Using curl

```bash
# Immediate scan with results
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",
    "scan_types": ["endpoints", "subdomains"]
  }'
```

#### Option B: Using Python

```python
import httpx

response = httpx.post(
    "http://localhost:8000/api/v1/scans/immediate",
    json={
        "url": "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",
        "scan_types": ["all_passive"]
    },
    timeout=60.0
)

results = response.json()
print(f"Found {len(results)} scan results")

for result in results:
    print(f"\n{result['scan_type']}:")
    for finding in result['findings']:
        print(f"  - {finding['title']}: {finding['match_count']} matches")
```

#### Option C: Using the Interactive Docs

1. Go to http://localhost:8000/docs
2. Click on "POST /api/v1/scans/immediate"
3. Click "Try it out"
4. Enter your request:
```json
{
  "url": "https://example.com/app.js",
  "scan_types": ["secrets", "endpoints"]
}
```
5. Click "Execute"

### 5. Check Task Status

```bash
# Get task summary
curl "http://localhost:8000/api/v1/tasks/summary"

# Get all tasks
curl "http://localhost:8000/api/v1/tasks/"

# Get completed tasks
curl "http://localhost:8000/api/v1/tasks/status/completed"
```

## 📊 Common Use Cases

### Scan for Secrets in a JavaScript File

```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/bundle.js",
    "scan_types": ["secrets"]
  }'
```

### Find API Endpoints

```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/api-client.js",
    "scan_types": ["endpoints"]
  }'
```

### Check for Dependency Confusion

```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/package.json",
    "scan_types": ["dependency_confusion"]
  }'
```

### Batch Scan Multiple Files

```bash
curl -X POST "http://localhost:8000/api/v1/scans/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": [
      "https://example.com/app.js",
      "https://example.com/vendor.js",
      "https://example.com/config.json"
    ],
    "scan_types": ["all_passive"]
  }'
```

### Run All Scans

```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/app.js",
    "scan_types": ["all_passive"]
  }'
```

## 🐳 Using Docker

### Build and Run

```bash
# Build image
docker build -t js-miner-api .

# Run container
docker run -p 8000:8000 js-miner-api

# Or use docker-compose
docker-compose up
```

### Access the API

The API will be available at http://localhost:8000

## 🔧 Configuration

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` to customize:

```bash
# Application
APP_NAME="JS Miner API"
APP_VERSION="2.0.0"
DEBUG=True
PORT=8000

# Logging
LOG_LEVEL=INFO
VERBOSE_LOGGING=True

# Scanner
MAX_WORKERS=10
SHANNON_ENTROPY_THRESHOLD=3.5
```

## 📝 Available Scan Types

| Scan Type | Description |
|-----------|-------------|
| `secrets` | Find API keys, tokens, passwords |
| `subdomains` | Discover subdomains |
| `cloud_urls` | Find cloud provider URLs |
| `dependency_confusion` | Check for vulnerable NPM packages |
| `endpoints` | Find REST API endpoints |
| `all_passive` | Run all passive scans (recommended) |
| `all` | Run all available scans |

## 🎯 Next Steps

1. **Read the full documentation:** [README_FASTAPI.md](README_FASTAPI.md)
2. **Understand the conversion:** [CONVERSION_NOTES.md](CONVERSION_NOTES.md)
3. **Explore the API:** http://localhost:8000/docs
4. **Integrate into your workflow:** Use the REST API in your tools

## 💡 Tips

- Use `all_passive` scan type for comprehensive analysis
- Check task summary regularly to monitor performance
- Clear completed tasks periodically to free memory
- Use immediate scans for quick results
- Use background scans for large batches

## 🐛 Troubleshooting

### Port already in use
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### Dependencies not installing
```bash
# Upgrade pip first
pip3.10 install --upgrade pip
pip3.10 install -r requirements.txt
```

### Permission denied on run.sh
```bash
chmod +x run.sh
./run.sh
```

### NPM registry connection issues
- Check your internet connection
- Verify NPM registry URLs in `.env`
- Some scans (dependency confusion) require NPM access

## 📞 Support

- Check logs for detailed error messages
- Review the API documentation at `/docs`
- See [CONVERSION_NOTES.md](CONVERSION_NOTES.md) for architecture details

## ✅ Verification

Test the installation:

```bash
# Health check
curl http://localhost:8000/health

# Should return:
# {"status": "healthy"}

# Root endpoint
curl http://localhost:8000/

# Should return:
# {"name": "JS Miner API", "version": "2.0.0", "status": "running"}
```

Success! You're ready to scan JavaScript files for security issues! 🎉
