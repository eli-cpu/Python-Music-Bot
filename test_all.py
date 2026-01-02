#!/usr/bin/env python3
"""
Simple test runner for all music bot tests.
Run this from the project root directory.
"""

import subprocess
import sys
import os

def run_test_suite():
    """Run the comprehensive test suite"""
    print("🎵 Music Bot - Complete Test Suite")
    print("=" * 60)

    test_script = "tests/run_tests.py"

    try:
        # Run the test suite
        result = subprocess.run([sys.executable, test_script],
                              cwd=os.path.dirname(__file__))

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run test suite: {e}")
        return False

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)