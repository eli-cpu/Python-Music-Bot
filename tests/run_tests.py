#!/usr/bin/env python3
"""
Run all test suites for the music bot.
"""

import subprocess
import sys
import os

def run_test(script_name, description):
    """Run a single test script"""
    print(f"\n{'='*20} Running {description} {'='*20}")

    try:
        result = subprocess.run([sys.executable, script_name],
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run {script_name}: {e}")
        return False

def main():
    """Run all tests"""
    print("🎵 Music Bot - Complete Test Suite")
    print("=" * 60)

    tests = [
        ("test_queue.py", "Queue System Tests"),
        ("test_streaming.py", "Streaming Functionality Tests"),
        ("test_audio.py", "Audio Pipeline Tests"),
        ("test_discord_bot.py", "Discord Bot Functionality Tests"),
    ]

    results = []

    for script, description in tests:
        success = run_test(script, description)
        results.append(success)

        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description}: {status}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 Complete Test Summary:")

    passed = sum(results)
    total = len(results)

    print(f"   Tests Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Your music bot is ready.")
        print("\n🚀 Next steps:")
        print("   1. Make sure FFmpeg is installed")
        print("   2. Set up your .env file with Discord and Spotify credentials")
        print("   3. Run: python bot.py")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("\n🔧 Common fixes:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Install FFmpeg: sudo apt install ffmpeg")
        print("   - Check your Spotify API credentials")

if __name__ == "__main__":
    main()