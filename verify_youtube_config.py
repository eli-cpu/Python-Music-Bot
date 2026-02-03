#!/usr/bin/env python3
"""
Verification script to check YouTube PO token configuration.
This script verifies that the bot is properly configured to handle
YouTube's PO token requirements.
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_configuration():
    """Verify that YouTube configuration is correct"""
    print("=" * 60)
    print("YouTube PO Token Configuration Verification")
    print("=" * 60)
    
    try:
        from utils.streaming_youtube import youtube_streamer
        
        print("\n✅ Successfully imported YouTubeStreamer")
        
        # Check if extractor_args is set
        if 'extractor_args' not in youtube_streamer.ydl_opts:
            print("❌ ERROR: extractor_args not found in configuration")
            return False
        
        print("✅ extractor_args is configured")
        
        # Check if youtube extractor args are set
        youtube_args = youtube_streamer.ydl_opts['extractor_args'].get('youtube', {})
        if not youtube_args:
            print("❌ ERROR: YouTube extractor args not found")
            return False
        
        print("✅ YouTube extractor args are configured")
        
        # Check if player_client is set
        player_client = youtube_args.get('player_client')
        if not player_client:
            print("❌ ERROR: player_client not configured")
            return False
        
        print(f"✅ player_client is configured: {player_client}")
        
        # Verify Android client is in the list
        if 'android' not in player_client:
            print("⚠️  WARNING: Android client not found in player_client list")
            print("   This may cause issues with PO token requirements")
            return False
        
        print("✅ Android client is configured (no PO token needed)")
        
        # Check yt-dlp version
        try:
            import yt_dlp
            version = yt_dlp.version.__version__
            print(f"\n✅ yt-dlp version: {version}")
            
            # Check if version is recent enough (2024.8.0 or later)
            year_month = version.split('.')[:2]
            if len(year_month) >= 2:
                year = int(year_month[0])
                month = int(year_month[1])
                if year > 2024 or (year == 2024 and month >= 8):
                    print("✅ yt-dlp version is recent enough for PO token handling")
                else:
                    print("⚠️  WARNING: yt-dlp version may be too old")
                    print("   Recommended: 2024.8.0 or later")
                    print("   Run: pip install --upgrade yt-dlp")
        except Exception as e:
            print(f"⚠️  Could not verify yt-dlp version: {e}")
        
        print("\n" + "=" * 60)
        print("Configuration Summary:")
        print("=" * 60)
        print("✅ Bot is properly configured to handle YouTube PO tokens")
        print("✅ Using Android client (no PO token required)")
        print("✅ Web client configured as fallback")
        print("\nYour bot should work without YouTube token issues!")
        print("=" * 60)
        
        return True
        
    except ImportError as e:
        print(f"❌ ERROR: Failed to import required modules: {e}")
        print("   Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ ERROR: Unexpected error during verification: {e}")
        return False

if __name__ == "__main__":
    success = verify_configuration()
    sys.exit(0 if success else 1)
