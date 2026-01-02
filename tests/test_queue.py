#!/usr/bin/env python3
"""
Test the music queue functionality without external dependencies.
"""

import sys
import os
from collections import deque

# Add the project directory to Python path (parent directory)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.streaming_spotify import Song, MusicPlayer

def test_song_class():
    """Test the Song class"""
    print("🧪 Testing Song class...")

    song = Song(
        title="Test Song",
        url="https://example.com",
        duration=180,
        thumbnail="https://example.com/thumb.jpg",
        requester="TestUser"
    )

    assert song.title == "Test Song"
    assert song.url == "https://example.com"
    assert song.duration == 180
    assert song.thumbnail == "https://example.com/thumb.jpg"
    assert song.requester == "TestUser"

    print("✅ Song class works correctly")
    return True

def test_queue_operations():
    """Test queue operations"""
    print("\n🧪 Testing queue operations...")

    music_player = MusicPlayer()

    # Test initial state
    assert len(music_player.queue) == 0
    assert music_player.current_song is None
    assert music_player.is_playing == False

    # Add songs to queue
    song1 = Song("Song 1", "url1", 100, requester="User1")
    song2 = Song("Song 2", "url2", 200, requester="User2")
    song3 = Song("Song 3", "url3", 300, requester="User3")

    music_player.queue.append(song1)
    music_player.queue.append(song2)
    music_player.queue.append(song3)

    assert len(music_player.queue) == 3
    print("✅ Added 3 songs to queue")

    # Test queue info
    queue_info = music_player.get_queue_info()
    assert len(queue_info['queue']) == 3
    assert queue_info['current'] is None
    assert queue_info['is_playing'] == False
    print("✅ Queue info retrieval works")

    # Test current song setting
    music_player.current_song = song1
    music_player.is_playing = True

    queue_info = music_player.get_queue_info()
    assert queue_info['current'] == song1
    assert queue_info['is_playing'] == True
    print("✅ Current song tracking works")

    # Test queue clearing
    music_player.clear_queue()
    assert len(music_player.queue) == 0
    print("✅ Queue clearing works")

    return True

def test_after_playing_callback():
    """Test the after playing callback"""
    print("\n🧪 Testing after playing callback...")

    music_player = MusicPlayer()

    # Set up a song and queue
    song1 = Song("Song 1", "url1", 100)
    song2 = Song("Song 2", "url2", 200)

    music_player.current_song = song1
    music_player.is_playing = True
    music_player.queue.append(song2)

    # Simulate song ending
    music_player._after_playing()

    assert music_player.current_song is None
    assert music_player.is_playing == False
    print("✅ After playing callback works")

    return True

async def test_async_queue_methods():
    """Test async queue methods"""
    print("\n🧪 Testing async queue methods...")

    music_player = MusicPlayer()
    song = Song("Test Song", "test_url", 150)

    await music_player.add_to_queue(song)
    assert len(music_player.queue) == 1
    assert music_player.queue[0] == song
    print("✅ Async queue addition works")

    return True

def main():
    """Run all queue tests"""
    print("🎵 Queue Functionality Test Suite")
    print("=" * 50)

    results = []

    # Test 1: Song class
    results.append(test_song_class())

    # Test 2: Queue operations
    results.append(test_queue_operations())

    # Test 3: After playing callback
    results.append(test_after_playing_callback())

    # Test 4: Async methods
    import asyncio
    results.append(asyncio.run(test_async_queue_methods()))

    # Summary
    print("\n" + "=" * 50)
    print("📊 Queue Test Results:")
    passed = sum(results)
    total = len(results)
    print(f"   Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All queue tests passed!")
    else:
        print("⚠️  Some queue tests failed.")

if __name__ == "__main__":
    main()