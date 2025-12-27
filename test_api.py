"""
Simple test script for JS Miner API
Run after starting the server to verify everything works
"""
import httpx
import time


def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = httpx.get("http://localhost:8000/health")
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_root():
    """Test root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = httpx.get("http://localhost:8000/")
        data = response.json()
        print(f"✅ Root endpoint: {data}")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False


def test_task_summary():
    """Test task summary endpoint"""
    print("\nTesting task summary endpoint...")
    try:
        response = httpx.get("http://localhost:8000/api/v1/tasks/summary")
        data = response.json()
        print(f"✅ Task summary: {data}")
        return True
    except Exception as e:
        print(f"❌ Task summary failed: {e}")
        return False


def test_simple_scan():
    """Test a simple scan"""
    print("\nTesting simple scan...")
    
    # Sample JavaScript content with some test data
    sample_js = """
    const apiKey = "test_api_key_12345";
    const endpoint = "/api/v1/users";
    
    function getUsers() {
        return fetch(endpoint);
    }
    
    const s3Bucket = "mybucket.s3.amazonaws.com";
    const subdomain = "api.example.com";
    """
    
    try:
        print("Sending scan request...")
        response = httpx.post(
            "http://localhost:8000/api/v1/scans/immediate",
            json={
                "url": "http://test.example.com/app.js",
                "content": sample_js,
                "scan_types": ["secrets", "endpoints", "cloud_urls", "subdomains"]
            },
            timeout=30.0
        )
        
        results = response.json()
        print(f"\n✅ Scan completed! Found {len(results)} scan results")
        
        for result in results:
            print(f"\n📊 {result['scan_type']}:")
            print(f"   Status: {result['status']}")
            print(f"   Findings: {len(result['findings'])}")
            
            for finding in result['findings']:
                print(f"   - {finding['title']}")
                print(f"     Severity: {finding['severity']}")
                print(f"     Confidence: {finding['confidence']}")
                print(f"     Matches: {finding['match_count']}")
                if finding['matches']:
                    print(f"     Examples: {finding['matches'][:3]}")
        
        return True
    except Exception as e:
        print(f"❌ Scan failed: {e}")
        return False


def test_batch_scan():
    """Test batch scanning"""
    print("\n\nTesting batch scan...")
    
    try:
        response = httpx.post(
            "http://localhost:8000/api/v1/scans/batch",
            json={
                "urls": [
                    "http://example.com/app1.js",
                    "http://example.com/app2.js"
                ],
                "scan_types": ["endpoints"]
            },
            timeout=10.0
        )
        
        data = response.json()
        print(f"✅ Batch scan initiated: {data}")
        
        # Wait a bit and check tasks
        time.sleep(2)
        response = httpx.get("http://localhost:8000/api/v1/tasks/summary")
        summary = response.json()
        print(f"   Task summary after batch: {summary}")
        
        return True
    except Exception as e:
        print(f"❌ Batch scan failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("JS Miner API Test Suite")
    print("=" * 60)
    print("\nMake sure the API is running on http://localhost:8000")
    print("Start it with: python3.10 -m uvicorn app.main:app --reload")
    print("\n" + "=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    results.append(("Task Summary", test_task_summary()))
    results.append(("Simple Scan", test_simple_scan()))
    results.append(("Batch Scan", test_batch_scan()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Total: {len(results)} tests | Passed: {passed} | Failed: {failed}")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above for details.")
    
    return failed == 0


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        exit(1)
