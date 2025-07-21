#!/usr/bin/env python3
"""
Test runner script for cheese manufacturing database
"""
import subprocess
import sys
from pathlib import Path

def run_test_suite():
    """Run all test suites"""
    test_dir = Path(__file__).parent
    
    print("🧪 Running Cheese Manufacturing Database Tests")
    print("=" * 50)
    
    # Run unit tests
    print("\n�� Running Unit Tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        str(test_dir / "unit"), 
        "-v", "--tb=short"
    ])
    
    if result.returncode != 0:
        print("❌ Unit tests failed")
        return False
    
    # Run integration tests
    print("\n🔗 Running Integration Tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        str(test_dir / "integration"), 
        "-v", "--tb=short"
    ])
    
    if result.returncode != 0:
        print("❌ Integration tests failed")
        return False
    
    # Run performance tests (optional)
    print("\n⚡ Running Performance Tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        str(test_dir / "performance"), 
        "-v", "--tb=short", "-m", "slow"
    ])
    
    if result.returncode != 0:
        print("⚠️  Performance tests failed (non-critical)")
    
    # Run E2E tests
    print("\n�� Running End-to-End Tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        str(test_dir / "e2e"), 
        "-v", "--tb=short"
    ])
    
    if result.returncode != 0:
        print("❌ E2E tests failed")
        return False
    
    print("\n✅ All critical tests passed!")
    return True

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1) 