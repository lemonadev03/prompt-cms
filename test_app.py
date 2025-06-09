#!/usr/bin/env python3
"""
Simple test to verify the Prompt CMS application setup
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    try:
        from app.main import app
        from app.models import Prompt
        from app.database import Base
        from app.auth import verify_password
        from app.admin import router as admin_router
        from app.public import router as public_router
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test that the FastAPI app can be created"""
    try:
        from app.main import app
        assert app.title == "Prompt CMS"
        print("✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_environment():
    """Test environment setup"""
    try:
        import asyncpg
        import sqlalchemy
        import fastapi
        import jinja2
        print("✅ All required packages available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Prompt CMS Setup...")
    print("-" * 40)
    
    tests = [
        test_environment,
        test_imports,
        test_app_creation,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("-" * 40)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! Your Prompt CMS is ready to run.")
        print("\nNext steps:")
        print("1. Set up your PostgreSQL database")
        print("2. Copy env.example to .env and configure")
        print("3. Run: alembic upgrade head")
        print("4. Run: uvicorn app.main:app --reload")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 