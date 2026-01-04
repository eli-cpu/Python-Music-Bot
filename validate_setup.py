#!/usr/bin/env python3
"""
Validation script to check if the music bot setup is correct.
This checks file structure, syntax, and basic imports without requiring installed dependencies.
"""

import os
import ast
import sys
from pathlib import Path

def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking file structure...")

    required_files = [
        "bot.py",
        "utils/__init__.py",
        "utils/streaming_spotify.py",
        "utils/streaming_youtube.py",
        "commands/__init__.py",
        "commands/play.py",
        "commands/join.py",
        "commands/leave.py",
        "commands/skip.py",
        "commands/stop.py",
        "commands/nowplaying.py",
        "commands/control.py",
        "commands/forward.py",
        "requirements.txt",
        "README.md",
        "test_all.py",
        "tests/test_queue.py",
        "tests/test_streaming.py",
        "tests/test_audio.py",
        "tests/test_discord_bot.py",
        "tests/run_tests.py"
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_python_syntax():
    """Check Python syntax of all .py files"""
    print("\n🐍 Checking Python syntax...")

    python_files = [
        "bot.py",
        "utils/__init__.py",
        "utils/streaming_spotify.py",
        "utils/streaming_youtube.py",
        "commands/__init__.py",
        "commands/play.py",
        "commands/join.py",
        "commands/leave.py",
        "commands/skip.py",
        "commands/stop.py",
        "commands/nowplaying.py",
        "commands/backward.py",
        "commands/pause.py",
        "commands/resume.py",
        "commands/queue.py",
        "commands/volume.py",
        "commands/clear.py",
        "commands/control.py",
        "test_all.py",
        "tests/test_queue.py",
        "tests/test_streaming.py",
        "tests/test_audio.py",
        "tests/test_discord_bot.py",
        "tests/run_tests.py"
    ]

    syntax_errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            syntax_errors.append(f"{file_path}: {e}")
        except Exception as e:
            syntax_errors.append(f"{file_path}: {e}")

    if syntax_errors:
        print(f"❌ Syntax errors found: {syntax_errors}")
        return False
    else:
        print("✅ All Python files have valid syntax")
        return True

def check_requirements_file():
    """Check if requirements.txt exists and has content"""
    print("\n📦 Checking requirements.txt...")

    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False

    with open("requirements.txt", 'r') as f:
        content = f.read().strip()

    if not content:
        print("❌ requirements.txt is empty")
        return False

    lines = content.split('\n')
    print(f"✅ requirements.txt contains {len(lines)} dependencies")
    for line in lines:
        if line.strip():
            print(f"   - {line.strip()}")

    return True

def check_readme_structure():
    """Check if README has the expected sections"""
    print("\n📖 Checking README.md structure...")

    if not os.path.exists("README.md"):
        print("❌ README.md not found")
        return False

    with open("README.md", 'r') as f:
        content = f.read()

    required_sections = [
        "# Discord Music Bot",
        "## Setup Instructions",
        "## Testing the Bot",
        "## Current Features"
    ]

    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)

    if missing_sections:
        print(f"❌ Missing README sections: {missing_sections}")
        return False
    else:
        print("✅ README.md has all required sections")
        return True

def check_test_structure():
    """Check test folder structure"""
    print("\n🧪 Checking test structure...")

    test_dir = Path("tests")
    if not test_dir.exists() or not test_dir.is_dir():
        print("❌ tests/ directory not found")
        return False

    test_files = list(test_dir.glob("test_*.py"))
    if len(test_files) < 4:
        print(f"❌ Expected at least 4 test files, found {len(test_files)}")
        return False

    print(f"✅ Found {len(test_files)} test files:")
    for test_file in sorted(test_files):
        print(f"   - {test_file.name}")

    return True

def main():
    """Run all validation checks"""
    print("🔍 Music Bot Setup Validation")
    print("=" * 50)

    checks = [
        check_file_structure,
        check_python_syntax,
        check_requirements_file,
        check_readme_structure,
        check_test_structure
    ]

    results = []
    for check_func in checks:
        results.append(check_func())

    # Summary
    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    passed = sum(results)
    total = len(results)
    print(f"   Checks passed: {passed}/{total}")

    if passed == total:
        print("🎉 Setup validation passed! Your bot is ready for testing.")
        print("\n🚀 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Install FFmpeg: sudo apt install ffmpeg")
        print("   3. Run tests: python test_all.py")
        print("   4. Start bot: python bot.py")
        return True
    else:
        print("⚠️  Setup validation failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)