#!/usr/bin/env python3
"""
Test script for the music streaming functionality.
This script tests the core streaming methods without requiring Discord.
"""

import os
import asyncio
import sys

# Add the project directory to Python path (parent directory)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.streaming_spotify import MusicPlayer

async def test_spotify_extraction():
    """Test Spotify URL extraction"""
    print("🧪 Testing Spotify URL extraction...")

    music_player = MusicPlayer()

    # Test Spotify URL
    spotify_url = "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC?si=abc123"
    result = music_player.extract_spotify_info(spotify_url)

    if result:
        print(f"✅ Spotify extraction successful:")
        print(f"   Title: {result['title']}")
        print(f"   Artist: {result['artist']}")
        print(f"   Search query: {result['query']}")
    else:
        print("❌ Spotify extraction failed - check your API credentials")

    return result is not None

async def test_youtube_search():
    """Test YouTube search functionality"""
    print("\n🧪 Testing YouTube search...")

    music_player = MusicPlayer()

    # Test search query
    query = "Never Gonna Give You Up"
    result = await music_player.search_youtube(query)

    if result:
        print(f"✅ YouTube search successful:")
        print(f"   Title: {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Duration: {result['duration']} seconds")
        print(f"   Direct URL: {result['direct_url'][:50]}...")
    else:
        print("❌ YouTube search failed")

    return result is not None

async def test_stream_url_extraction():
    """Test extracting streaming URL from YouTube"""
    print("\n🧪 Testing stream URL extraction...")

    music_player = MusicPlayer()

    # Use a known working YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll

    try:
        import yt_dlp
        ydl = yt_dlp.YoutubeDL(music_player.ydl_opts)
        loop = asyncio.get_event_loop()

        # Extract info
        info = await loop.run_in_executor(None, lambda: ydl.extract_info(youtube_url, download=False))

        if info and 'url' in info:
            print(f"✅ Stream URL extraction successful:")
            print(f"   Title: {info.get('title', 'Unknown')}")
            print(f"   Duration: {info.get('duration', 'Unknown')} seconds")
            print(f"   Stream URL: {info['url'][:50]}...")
            print(f"   Format: {info.get('format', 'Unknown')}")
            return True
        else:
            print("❌ Failed to extract stream URL")
            return False

    except Exception as e:
        print(f"❌ Error extracting stream URL: {e}")
        return False

async def test_spotify_to_youtube_flow():
    """Test the complete flow: Spotify URL -> YouTube search -> Stream URL"""
    print("\n🧪 Testing complete Spotify to YouTube flow...")

    music_player = MusicPlayer()

    # Test with a Spotify URL
    spotify_url = "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC?si=abc123"

    # Step 1: Extract Spotify info
    spotify_info = music_player.extract_spotify_info(spotify_url)
    if not spotify_info:
        print("❌ Step 1 failed: Spotify extraction")
        return False

    print(f"✅ Step 1: Spotify info extracted - {spotify_info['title']} by {spotify_info['artist']}")

    # Step 2: Search YouTube
    youtube_result = await music_player.search_youtube(spotify_info['query'])
    if not youtube_result:
        print("❌ Step 2 failed: YouTube search")
        return False

    print(f"✅ Step 2: YouTube video found - {youtube_result['title']}")

    # Step 3: Extract stream URL
    try:
        import yt_dlp
        ydl = yt_dlp.YoutubeDL(music_player.ydl_opts)
        loop = asyncio.get_event_loop()

        info = await loop.run_in_executor(None, lambda: ydl.extract_info(youtube_result['url'], download=False))

        if info and 'url' in info:
            print(f"✅ Step 3: Stream URL extracted successfully")
            print(f"   Ready to stream: {info['url'][:50]}...")
            return True
        else:
            print("❌ Step 3 failed: Stream URL extraction")
            return False

    except Exception as e:
        print(f"❌ Step 3 failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🎵 Music Streaming Test Suite")
    print("=" * 50)

    # Check if required dependencies are available
    try:
        import yt_dlp
        import spotipy
        print("✅ Required dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install yt-dlp spotipy requests")
        return

    # Check environment variables
    spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
    spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not spotify_id or not spotify_secret:
        print("⚠️  Spotify credentials not found in environment variables")
        print("   Spotify URL tests will fail, but YouTube tests should work")
    else:
        print("✅ Spotify credentials found")

    print("\n" + "=" * 50)

    # Run tests
    results = []

    # Test 1: Spotify extraction
    results.append(await test_spotify_extraction())

    # Test 2: YouTube search
    results.append(await test_youtube_search())

    # Test 3: Stream URL extraction
    results.append(await test_stream_url_extraction())

    # Test 4: Complete flow
    if spotify_id and spotify_secret:
        results.append(await test_spotify_to_youtube_flow())
    else:
        print("\n⏭️  Skipping complete flow test (no Spotify credentials)")

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    passed = sum(results)
    total = len(results)
    print(f"   Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Your streaming functionality should work.")
    else:
        print("⚠️  Some tests failed. Check your API credentials and network connection.")

    print("\n💡 Next steps:")
    print("   1. Fix any failed tests")
    print("   2. Install FFmpeg: sudo apt install ffmpeg")
    print("   3. Run the Discord bot: python bot.py")

if __name__ == "__main__":
    asyncio.run(main())