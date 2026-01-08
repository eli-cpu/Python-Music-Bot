#!/usr/bin/env python3
"""
Quick test for Spotify oEmbed functionality (no API keys required)
"""

import asyncio
import aiohttp
import re
import sys

async def extract_spotify_info_oembed(url):
    """Extract track information from Spotify URL using oEmbed (no API key required)"""
    # Extract track ID from Spotify URL
    match = re.search(r'spotify\.com/track/([a-zA-Z0-9]+)', url)
    if not match:
        return None

    try:
        # Use Spotify's oEmbed endpoint (no API key required)
        oembed_url = f"https://open.spotify.com/oembed?url={url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(oembed_url) as response:
                if response.status == 200:
                    data = await response.json()

                    # Debug: print the raw response
                    print(f"Raw oEmbed data: {data}")

                    # Extract title from oEmbed data
                    title_text = data.get('title', '')

                    # Spotify oEmbed only provides the track title, not the artist
                    # We'll use just the title for YouTube search - it should be sufficient
                    # for most popular songs
                    return {
                        'title': title_text,
                        'artist': 'Unknown (from Spotify)',  # Placeholder
                        'query': title_text  # Search YouTube with just the title
                    }
                else:
                    print(f"oEmbed request failed with status: {response.status}")
                    return None

    except Exception as e:
        print(f"Error extracting Spotify info via oEmbed: {e}")
        return None

async def test_spotify_oembed():
    """Test Spotify oEmbed extraction"""
    print("🧪 Testing Spotify oEmbed functionality...")

    # Test with a popular Spotify track
    spotify_url = "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC"  # Never Gonna Give You Up

    print(f"Testing URL: {spotify_url}")

    try:
        result = await extract_spotify_info_oembed(spotify_url)

        if result:
            print("✅ Successfully extracted Spotify info:")
            print(f"   Title: {result['title']}")
            print(f"   Artist: {result['artist']}")
            print(f"   Search Query: {result['query']}")
            return True
        else:
            print("❌ Failed to extract Spotify info")
            return False

    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_spotify_oembed())
    sys.exit(0 if success else 1)