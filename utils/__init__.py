"""
Music Bot Utilities Package

This package contains utilities for music streaming functionality:
- streaming_spotify.py: Spotify integration and music player
- streaming_youtube.py: YouTube streaming functionality
"""

from .streaming_spotify import music_player, Song, MusicPlayer
from .streaming_youtube import youtube_streamer, YouTubeStreamer

__all__ = [
    'music_player',
    'Song',
    'MusicPlayer',
    'youtube_streamer',
    'YouTubeStreamer'
]