#!/usr/bin/env python3

import sys
import subprocess
import os

def run_tests():
    """Run the test suite with various options"""
    
    # Check if pytest is available
    try:
        import pytest
    except ImportError:
        print("pytest not found. Installing test dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "test_requirements.txt"])
    
    # Run tests with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "--verbose",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html",
        "test_samsung_remote.py"
    ]
    
    print("Running tests with coverage...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

def run_specific_test(test_name):
    """Run a specific test"""
    cmd = [
        sys.executable, "-m", "pytest",
        f"test_samsung_remote.py::{test_name}",
        "-v"
    ]
    
    print(f"Running test: {test_name}")
    subprocess.run(cmd)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage:")
            print("  python run_tests.py              # Run all tests")
            print("  python run_tests.py <test_name>  # Run specific test")
            print("\nAvailable test classes:")
            print("  TestTVInfo")
            print("  TestTVCon") 
            print("  TestSSDP")
            print("  TestMacro")
            print("  TestSamsungRemote")
            print("  TestIntegration")
        else:
            run_specific_test(sys.argv[1])
    else:
        run_tests()
