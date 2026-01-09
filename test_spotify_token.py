#!/usr/bin/env python3
"""
Test Spotify token authentication functionality
"""

import os
import sys
import asyncio

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.streaming_spotify import MusicPlayer

async def test_spotify_token():
    """Test Spotify token-based authentication"""
    print("🧪 Testing Spotify token authentication...")

    # Check what authentication method is being used
    token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    print(f"🔑 Access Token: {'Set' if token else 'Not set'}")
    print(f"🔑 Client ID: {'Set' if client_id else 'Not set'}")
    print(f"🔑 Client Secret: {'Set' if client_secret else 'Not set'}")

    # Create music player instance
    player = MusicPlayer()

    if player.spotify:
        auth_method = "Access Token" if token else "Client Credentials"
        print(f"✅ Spotify client initialized successfully using {auth_method}")

        # Test with a Spotify URL
        spotify_url = "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC"  # Never Gonna Give You Up
        print(f"\n🎵 Testing URL: {spotify_url}")

        result = await player.extract_spotify_info(spotify_url)

        if result:
            print("✅ Successfully extracted Spotify info:")
            print(f"   Title: {result['title']}")
            print(f"   Artist: {result['artist']}")
            print(f"   Search Query: {result['query']}")

            if result['artist'] != 'Unknown (from Spotify)':
                print("🎉 Full metadata extracted! (Title + Artist)")
            else:
                print("📝 Using oEmbed fallback (Title only)")
        else:
            print("❌ Failed to extract information")
    else:
        print("⚠️  No Spotify authentication available - using oEmbed fallback")

        # Test oEmbed fallback
        spotify_url = "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC"
        print(f"\n🎵 Testing oEmbed fallback with URL: {spotify_url}")

        result = await player.extract_spotify_info(spotify_url)

        if result:
            print("✅ oEmbed extraction successful:")
            print(f"   Title: {result['title']}")
            print(f"   Artist: {result['artist']} (placeholder)")
            print(f"   Search Query: {result['query']}")
        else:
            print("❌ oEmbed extraction failed")

if __name__ == "__main__":
    asyncio.run(test_spotify_token())