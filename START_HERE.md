# 🚀 START HERE - Burp JS Miner FastAPI

Welcome! This is your complete guide to getting started with the FastAPI version of Burp JS Miner.

---

## ⚡ Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Start the Server
```bash
./run.sh
# or
python3 -m uvicorn app.main:app --reload
```

### 3. Open Your Browser
Go to: **http://localhost:8000/docs**

### 4. Try a Scan
```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/app.js",
    "scan_types": ["all_passive"]
  }'
```

**Done!** 🎉

---

## 📚 Documentation Guide

Choose your path based on what you need:

### 🏃 I want to start using it NOW
→ Read: **[QUICKSTART.md](QUICKSTART.md)**
- Installation instructions
- First scan in 5 minutes
- Common use cases
- Troubleshooting

### 📖 I want to understand the API
→ Read: **[README_FASTAPI.md](README_FASTAPI.md)**
- Complete API documentation
- All endpoints explained
- Request/response examples
- Architecture overview
- Deployment options

### 🔧 I want technical details
→ Read: **[CONVERSION_NOTES.md](CONVERSION_NOTES.md)**
- How the conversion was done
- Original vs new architecture
- Technical decisions
- Implementation details
- Design patterns used

### 📊 I want a summary
→ Read: **[SUMMARY.md](SUMMARY.md)**
- What was converted
- File structure
- Features comparison
- Quick overview

### ✅ I want to verify installation
→ Run: **`python3 verify_installation.py`**
- Checks Python version
- Verifies file structure
- Tests dependencies
- Validates modules

---

## 🎯 What Is This?

This is a **FastAPI REST API** conversion of the popular **Burp Suite JS Miner** extension.

### What Does It Do?

Scans JavaScript and JSON files to find:
- 🔐 **Secrets** (API keys, tokens, passwords)
- 🌐 **Subdomains** (domain discovery)
- ☁️ **Cloud URLs** (AWS, Azure, Google Cloud, etc.)
- 📦 **Dependency Confusion** (vulnerable NPM packages)
- 🔗 **API Endpoints** (REST endpoints)

### Why FastAPI Version?

| Feature | Burp Extension | FastAPI API |
|---------|---------------|-------------|
| Platform | Burp Suite only | Any HTTP client |
| Integration | Manual | Automated |
| CI/CD | ❌ | ✅ |
| Batch Scans | Limited | ✅ |
| API Access | ❌ | ✅ |
| Scalability | Single instance | Horizontal |

---

## 🗂️ Project Structure

```
workspace/
├── app/                    # Main application
│   ├── main.py            # FastAPI app
│   ├── config.py          # Configuration
│   ├── api/               # API endpoints
│   ├── core/              # Business logic
│   ├── scanners/          # Security scanners
│   ├── models/            # Data models
│   └── utils/             # Utilities
├── requirements.txt        # Dependencies
├── .env.example           # Configuration template
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker Compose
├── run.sh                 # Start script
├── verify_installation.py # Verification
├── test_api.py            # Tests
└── Documentation/
    ├── START_HERE.md      ← You are here
    ├── QUICKSTART.md      ← Start here
    ├── README_FASTAPI.md  ← Full docs
    ├── CONVERSION_NOTES.md
    ├── SUMMARY.md
    └── CONVERSION_COMPLETE.md
```

---

## 🛠️ Installation Options

### Option 1: Traditional (Recommended)
```bash
# Install dependencies
pip3 install -r requirements.txt

# Start server
python3 -m uvicorn app.main:app --reload

# Test
python3 test_api.py
```

### Option 2: Using Run Script
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Docker
```bash
docker-compose up
```

---

## 🎓 Learning Path

### For Burp Suite Users

1. **Understand the Differences**
   - Burp menu items → API endpoints
   - Right-click → HTTP POST
   - Burp issues → JSON responses

2. **Try the API**
   - Open http://localhost:8000/docs
   - Try "POST /api/v1/scans/immediate"
   - See results in JSON

3. **Integrate**
   - Add to your workflow
   - Automate with scripts
   - CI/CD integration

### For API Users

1. **Start the Server**
   ```bash
   ./run.sh
   ```

2. **Explore the Docs**
   - Go to http://localhost:8000/docs
   - Try each endpoint
   - See request/response schemas

3. **Make Your First Request**
   ```python
   import httpx
   
   response = httpx.post(
       "http://localhost:8000/api/v1/scans/immediate",
       json={
           "url": "https://example.com/app.js",
           "scan_types": ["secrets"]
       }
   )
   print(response.json())
   ```

---

## 📋 Common Tasks

### Scan a Single File
```bash
curl -X POST "http://localhost:8000/api/v1/scans/immediate" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/app.js", "scan_types": ["secrets"]}'
```

### Batch Scan Multiple Files
```bash
curl -X POST "http://localhost:8000/api/v1/scans/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com/app.js", "https://example.com/vendor.js"],
    "scan_types": ["all_passive"]
  }'
```

### Check Task Status
```bash
curl "http://localhost:8000/api/v1/tasks/summary"
```

### Health Check
```bash
curl "http://localhost:8000/health"
```

---

## 🔍 Available Scans

| Scan Type | What It Finds | Use Case |
|-----------|---------------|----------|
| `secrets` | API keys, tokens, passwords | Security audit |
| `subdomains` | Subdomains | Reconnaissance |
| `cloud_urls` | Cloud provider URLs | Asset discovery |
| `dependency_confusion` | Vulnerable NPM packages | Supply chain security |
| `endpoints` | REST API endpoints | API discovery |
| `all_passive` | All of the above | Comprehensive scan |

---

## ⚙️ Configuration

Copy and edit `.env`:
```bash
cp .env.example .env
nano .env
```

Key settings:
- `PORT=8000` - Server port
- `LOG_LEVEL=INFO` - Logging level
- `MAX_WORKERS=10` - Concurrent scans
- `SHANNON_ENTROPY_THRESHOLD=3.5` - Secret detection sensitivity

---

## 🧪 Testing

### Verify Installation
```bash
python3 verify_installation.py
```

### Run Test Suite
```bash
python3 test_api.py
```

### Manual Test
```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

---

## 🚨 Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Use different port
uvicorn app.main:app --port 8001
```

### Dependencies Not Installing
```bash
# Upgrade pip
pip3 install --upgrade pip

# Install again
pip3 install -r requirements.txt
```

### Import Errors
```bash
# Verify installation
python3 verify_installation.py

# Check Python version (needs 3.10+)
python3 --version
```

---

## 📞 Getting Help

1. **Check Documentation**
   - [QUICKSTART.md](QUICKSTART.md) - Getting started
   - [README_FASTAPI.md](README_FASTAPI.md) - Full docs
   - [CONVERSION_NOTES.md](CONVERSION_NOTES.md) - Technical details

2. **Run Verification**
   ```bash
   python3 verify_installation.py
   ```

3. **Check Logs**
   - Server logs show detailed error messages
   - Set `LOG_LEVEL=DEBUG` for more detail

4. **Test Suite**
   ```bash
   python3 test_api.py
   ```

---

## ✅ Pre-flight Checklist

Before first use:

- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`pip3 install -r requirements.txt`)
- [ ] Verification passed (`python3 verify_installation.py`)
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Health check passes (`curl http://localhost:8000/health`)

---

## 🎯 Next Steps After Installation

1. **Explore the API**
   - Open http://localhost:8000/docs
   - Try each endpoint interactively
   
2. **Run Your First Scan**
   - Use the examples in [QUICKSTART.md](QUICKSTART.md)
   - Start with `all_passive` scan type
   
3. **Integrate Into Workflow**
   - Add to CI/CD pipeline
   - Create automation scripts
   - Set up monitoring

4. **Customize**
   - Edit `.env` for your needs
   - Adjust scan thresholds
   - Configure logging

---

## 🌟 Features Highlight

### Security Scanning
- ✅ Shannon entropy for secret detection
- ✅ NPM registry verification
- ✅ Multiple cloud providers
- ✅ Comprehensive regex patterns

### API Features
- ✅ OpenAPI/Swagger docs
- ✅ Async/await for performance
- ✅ Batch processing
- ✅ Task management
- ✅ Health checks

### Developer Experience
- ✅ Type hints
- ✅ Comprehensive docs
- ✅ Test suite
- ✅ Docker support
- ✅ Quick start script

---

## 📈 Performance

- **Concurrent Scanning:** Multiple scans run simultaneously
- **Async I/O:** Non-blocking HTTP requests
- **Connection Pooling:** Efficient HTTP client
- **Configurable Workers:** Adjust for your needs

---

## 🔒 Security

- **Shannon Entropy:** Reduces false positives
- **NPM Verification:** Real-time package checking
- **CORS Enabled:** Configurable cross-origin access
- **Error Handling:** Secure error messages

---

## 📊 Status

**✅ CONVERSION COMPLETE**
**✅ PRODUCTION READY**
**✅ FULLY TESTED**

---

## 🎉 You're Ready!

Choose your path:

1. **Quick Start** → [QUICKSTART.md](QUICKSTART.md)
2. **Full Documentation** → [README_FASTAPI.md](README_FASTAPI.md)
3. **Technical Details** → [CONVERSION_NOTES.md](CONVERSION_NOTES.md)
4. **Just Start**
   ```bash
   pip3 install -r requirements.txt
   ./run.sh
   # Open http://localhost:8000/docs
   ```

**Happy Scanning! 🚀**
