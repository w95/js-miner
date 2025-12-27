#!/usr/bin/env python3.10
"""
Installation Verification Script for JS Miner FastAPI

Run this script to verify your installation is complete and correct.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        return False


def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/api/__init__.py",
        "app/api/scans.py",
        "app/api/tasks.py",
        "app/core/__init__.py",
        "app/core/scanner_builder.py",
        "app/core/task_repository.py",
        "app/models/__init__.py",
        "app/models/schemas.py",
        "app/scanners/__init__.py",
        "app/scanners/base.py",
        "app/scanners/secrets.py",
        "app/scanners/subdomains.py",
        "app/scanners/cloud_urls.py",
        "app/scanners/dependency_confusion.py",
        "app/scanners/endpoints.py",
        "app/utils/__init__.py",
        "app/utils/constants.py",
        "app/utils/helpers.py",
        "requirements.txt",
        ".env.example",
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
            print(f"   ❌ Missing: {file}")
        else:
            print(f"   ✅ {file}")
    
    if missing:
        print(f"\n   ⚠️  {len(missing)} file(s) missing!")
        return False
    else:
        print(f"\n   ✅ All {len(required_files)} required files present")
        return True


def check_dependencies():
    """Check if dependencies can be imported"""
    print("\n📦 Checking dependencies...")
    
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("pydantic_settings", "Pydantic Settings"),
        ("httpx", "HTTPX"),
        ("regex", "Regex"),
    ]
    
    missing = []
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} not installed")
            missing.append(module_name)
    
    if missing:
        print(f"\n   ⚠️  {len(missing)} dependency(ies) missing!")
        print(f"   Run: pip3.10 install -r requirements.txt")
        return False
    else:
        print(f"\n   ✅ All dependencies installed")
        return True


def check_app_imports():
    """Check if app modules can be imported"""
    print("\n🔍 Checking app modules...")
    
    modules = [
        "app.main",
        "app.config",
        "app.api.scans",
        "app.api.tasks",
        "app.core.scanner_builder",
        "app.core.task_repository",
        "app.models.schemas",
        "app.scanners.secrets",
        "app.scanners.subdomains",
        "app.scanners.cloud_urls",
        "app.scanners.dependency_confusion",
        "app.scanners.endpoints",
        "app.utils.constants",
        "app.utils.helpers",
    ]
    
    errors = []
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except Exception as e:
            print(f"   ❌ {module}: {str(e)}")
            errors.append((module, str(e)))
    
    if errors:
        print(f"\n   ⚠️  {len(errors)} module(s) have import errors!")
        return False
    else:
        print(f"\n   ✅ All modules can be imported")
        return True


def check_env_file():
    """Check environment configuration"""
    print("\n⚙️  Checking environment configuration...")
    
    if Path(".env").exists():
        print("   ✅ .env file exists")
        return True
    elif Path(".env.example").exists():
        print("   ⚠️  .env file not found")
        print("   ℹ️  Copy .env.example to .env for custom configuration")
        print("   ℹ️  App will use defaults from .env.example")
        return True
    else:
        print("   ❌ Neither .env nor .env.example found")
        return False


def check_documentation():
    """Check if documentation files exist"""
    print("\n📚 Checking documentation...")
    
    docs = [
        "README_FASTAPI.md",
        "QUICKSTART.md",
        "CONVERSION_NOTES.md",
        "SUMMARY.md",
    ]
    
    found = 0
    for doc in docs:
        if Path(doc).exists():
            print(f"   ✅ {doc}")
            found += 1
        else:
            print(f"   ⚠️  {doc} not found")
    
    print(f"\n   ℹ️  {found}/{len(docs)} documentation files present")
    return True


def print_summary(checks):
    """Print summary of checks"""
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for check in checks.values() if check)
    total = len(checks)
    
    for name, result in checks.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} checks passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 Installation verified successfully!")
        print("\nNext steps:")
        print("1. Start the server:")
        print("   ./run.sh")
        print("   OR")
        print("   python3.10 -m uvicorn app.main:app --reload")
        print("\n2. Open your browser:")
        print("   http://localhost:8000/docs")
        print("\n3. Try a test scan:")
        print("   python3.10 test_api.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} check(s) failed")
        print("\nPlease fix the issues above before running the application.")
        return False


def main():
    """Main verification function"""
    print("=" * 60)
    print("JS Miner FastAPI - Installation Verification")
    print("=" * 60)
    
    checks = {
        "Python Version": check_python_version(),
        "File Structure": check_file_structure(),
        "Dependencies": check_dependencies(),
        "App Modules": check_app_imports(),
        "Environment Config": check_env_file(),
        "Documentation": check_documentation(),
    }
    
    success = print_summary(checks)
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\nVerification interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Verification error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
