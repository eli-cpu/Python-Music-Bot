import asyncio
import yt_dlp
import discord

class YouTubeStreamer:
    """Handles YouTube streaming functionality"""

    def __init__(self):
        # yt-dlp options optimized for real-time streaming
        self.ydl_opts = {
            'format': 'bestaudio[abr<=128]/bestaudio/best[height<=480]',  # Prioritize audio, fallback to video
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '128K',  # Explicit audio quality
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'buffersize': 1024,
            'http_chunk_size': 1048576,  # 1MB chunks for better streaming
            'retries': 10,
            'fragment_retries': 10,
            'skip_unavailable_fragments': True,
            'keepvideo': False,  # Don't keep video if audio-only is available
            'prefer_ffmpeg': True,  # Better streaming performance
        }

    async def search_youtube(self, query):
        """Search YouTube and return video info"""
        loop = asyncio.get_event_loop()
        ydl = yt_dlp.YoutubeDL(self.ydl_opts)

        try:
            # Run yt-dlp search in thread pool
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch:{query}", download=False))

            if 'entries' in info and info['entries']:
                video = info['entries'][0]
                return {
                    'title': video['title'],
                    'url': video['webpage_url'],
                    'duration': video.get('duration', 0),
                    'thumbnail': video.get('thumbnail'),
                    'direct_url': video['url']
                }
        except Exception as e:
            print(f"Error searching YouTube: {e}")

        return None

    async def get_stream_url(self, url):
        """Get streaming URL from YouTube video URL"""
        loop = asyncio.get_event_loop()
        ydl = yt_dlp.YoutubeDL(self.ydl_opts)

        try:
            # Extract audio info for streaming
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))

            if info and 'url' in info:
                return info['url']
        except Exception as e:
            print(f"Error getting stream URL: {e}")

        return None

    async def stream_audio(self, voice_client, stream_url, after_callback=None):
        """Stream audio to Discord voice channel"""
        try:
            # Create FFmpeg audio source with optimized streaming options
            audio_source = discord.FFmpegPCMAudio(
                stream_url,
                options='-vn -b:a 128k -bufsize 1024k -probesize 1024k -analyzeduration 0'
            )

            # Stop any currently playing audio
            if voice_client.is_playing():
                voice_client.stop()

            # Start streaming the audio
            if after_callback:
                voice_client.play(audio_source, after=after_callback)
            else:
                voice_client.play(audio_source)

            return True

        except Exception as e:
            print(f"Error streaming audio: {e}")
            return False

# Create global YouTube streamer instance
youtube_streamer = YouTubeStreamer()