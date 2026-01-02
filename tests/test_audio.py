#!/usr/bin/env python3
"""
Test FFmpeg audio streaming without Discord.
This tests if the audio stream URLs work with FFmpeg directly.
"""

import os
import asyncio
import subprocess
import sys

# Add the project directory to Python path (parent directory)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import MusicPlayer

async def test_ffmpeg_availability():
    """Test if FFmpeg is available"""
    print("🧪 Testing FFmpeg availability...")

    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
            # Print version info
            version_line = result.stdout.split('\n')[0]
            print(f"   Version: {version_line}")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ FFmpeg not found. Install with: sudo apt install ffmpeg")
        return False

async def test_audio_stream():
    """Test if we can stream audio using FFmpeg directly"""
    print("\n🧪 Testing audio stream extraction...")

    music_player = MusicPlayer()

    # Use a short test video
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (short)

    try:
        import yt_dlp
        ydl = yt_dlp.YoutubeDL(music_player.ydl_opts)
        loop = asyncio.get_event_loop()

        print("   Extracting stream info...")
        info = await loop.run_in_executor(None, lambda: ydl.extract_info(test_url, download=False))

        if info and 'url' in info:
            stream_url = info['url']
            print(f"✅ Stream URL extracted: {stream_url[:50]}...")

            # Test FFmpeg with the stream URL (just probe, don't play)
            print("   Testing FFmpeg stream processing...")
            ffmpeg_cmd = [
                'ffmpeg', '-i', stream_url,
                '-f', 'null', '-',  # Output to null (no file)
                '-t', '5'  # Only process first 5 seconds
            ]

            result = await asyncio.create_subprocess_exec(
                *ffmpeg_cmd,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                print("✅ FFmpeg can process the audio stream")
                print("   Audio format and stream are valid")
                return True
            else:
                print("❌ FFmpeg failed to process stream")
                if stderr:
                    error_lines = stderr.decode().split('\n')[-5:]  # Last 5 lines
                    print(f"   FFmpeg error: {error_lines}")
                return False
        else:
            print("❌ Failed to extract stream URL")
            return False

    except Exception as e:
        print(f"❌ Error testing audio stream: {e}")
        return False

async def test_discord_ffmpeg_import():
    """Test if Discord's FFmpegPCMAudio can be imported"""
    print("\n🧪 Testing Discord FFmpeg integration...")

    try:
        import discord
        from discord import FFmpegPCMAudio

        # Test creating FFmpegPCMAudio object (without actually using it)
        test_url = "https://example.com/audio.mp3"  # Dummy URL
        audio = FFmpegPCMAudio(test_url, options='-vn')

        print("✅ Discord FFmpegPCMAudio import successful")
        print(f"   FFmpegPCMAudio class: {FFmpegPCMAudio}")
        return True

    except ImportError as e:
        print(f"❌ Discord import failed: {e}")
        print("   Install with: pip install discord.py")
        return False
    except Exception as e:
        print(f"❌ FFmpegPCMAudio test failed: {e}")
        return False

async def main():
    """Run audio tests"""
    print("🎵 Audio Pipeline Test Suite")
    print("=" * 50)

    results = []

    # Test 1: FFmpeg availability
    results.append(await test_ffmpeg_availability())

    # Test 2: Audio stream extraction
    results.append(await test_audio_stream())

    # Test 3: Discord FFmpeg integration
    results.append(await test_discord_ffmpeg_import())

    # Summary
    print("\n" + "=" * 50)
    print("📊 Audio Test Results:")
    passed = sum(results)
    total = len(results)
    print(f"   Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All audio tests passed! Ready for Discord bot.")
        print("\n🚀 You can now run: python bot.py")
    else:
        print("⚠️  Some audio tests failed.")
        print("\n🔧 Troubleshooting:")
        print("   - Install FFmpeg: sudo apt install ffmpeg")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Check network connectivity")

if __name__ == "__main__":
    asyncio.run(main())