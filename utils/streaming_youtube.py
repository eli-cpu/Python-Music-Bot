import asyncio
import yt_dlp
import discord

class YouTubeStreamer:
    """Handles YouTube streaming functionality"""

    def __init__(self):
        # yt-dlp options optimized for real-time streaming with better error handling
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
            # Additional options for better stability
            'socket_timeout': 30,  # Connection timeout
            'extractor_retries': 3,  # Retry extracting info
            'file_access_retries': 3,  # Retry file access
            'concurrent_fragment_downloads': 1,  # Avoid overloading
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

    async def stream_audio(self, voice_client, stream_url, after_callback=None, start_time=0, max_retries=3):
        """Stream audio to Discord voice channel from a specific start time with retry logic"""
        last_error = None

        for attempt in range(max_retries):
            try:
                # Create FFmpeg audio source with optimized streaming options for stability
                # Added options to handle network interruptions and buffering better
                ffmpeg_options = (
                    '-vn -b:a 128k -bufsize 2048k -probesize 2048k -analyzeduration 5000000 '
                    '-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5 '
                    '-timeout 30000000 -rw_timeout 30000000'  # 30 second timeouts
                )

                if start_time > 0:
                    ffmpeg_options = f'-ss {start_time} {ffmpeg_options}'

                print(f"Attempting to stream audio (attempt {attempt + 1}/{max_retries})")

                audio_source = discord.FFmpegPCMAudio(
                    stream_url,
                    options=ffmpeg_options,
                    before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
                )

                # Stop any currently playing audio
                if voice_client.is_playing():
                    voice_client.stop()

                # Small delay to ensure clean state
                await asyncio.sleep(0.1)

                # Start streaming the audio
                if after_callback:
                    voice_client.play(audio_source, after=after_callback)
                else:
                    voice_client.play(audio_source)

                print(f"Successfully started audio stream (attempt {attempt + 1})")
                return True

            except Exception as e:
                last_error = e
                print(f"Stream attempt {attempt + 1} failed: {e}")

                # If this isn't the last attempt, wait before retrying
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)  # Brief pause before retry

        # All attempts failed
        print(f"All {max_retries} stream attempts failed. Last error: {last_error}")
        return False

# Create global YouTube streamer instance
youtube_streamer = YouTubeStreamer()