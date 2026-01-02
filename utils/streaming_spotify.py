import os
import re
import discord
from collections import deque

# Import YouTube streamer
from .streaming_youtube import youtube_streamer

# Get Spotify credentials from environment
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

class Song:
    def __init__(self, title, url, duration, thumbnail=None, requester=None):
        self.title = title
        self.url = url
        self.duration = duration
        self.thumbnail = thumbnail
        self.requester = requester

class MusicPlayer:
    def __init__(self):
        self.queue = deque()
        self.history = deque(maxlen=10)  # Keep last 10 songs for backward functionality
        self.current_song = None
        self.voice_client = None
        self.is_playing = False
        self.volume = 0.5
        self.last_text_channel = None  # Store last text channel for notifications

        # Initialize Spotify client
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            try:
                import spotipy
                from spotipy.oauth2 import SpotifyClientCredentials

                client_credentials_manager = SpotifyClientCredentials(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET
                )
                self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            except Exception as e:
                print(f"Failed to initialize Spotify client: {e}")
                self.spotify = None
        else:
            print("Spotify credentials not found. Spotify links won't work.")
            self.spotify = None

    def extract_spotify_info(self, url):
        """Extract track information from Spotify URL"""
        if not self.spotify:
            return None

        # Extract track ID from Spotify URL
        match = re.search(r'spotify\.com/track/([a-zA-Z0-9]+)', url)
        if not match:
            return None

        track_id = match.group(1)

        try:
            track = self.spotify.track(track_id)
            return {
                'title': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'query': f"{track['name']} {track['artists'][0]['name']}"
            }
        except Exception as e:
            print(f"Error extracting Spotify info: {e}")
            return None

    async def search_youtube(self, query):
        """Search YouTube and return video info using the YouTube streamer"""
        return await youtube_streamer.search_youtube(query)

    async def stream_and_play(self, interaction, song):
        """Stream and play a song"""
        if not interaction.user.voice:
            await interaction.followup.send("❌ You must be in a voice channel to play music!")
            return

        # Store the text channel for future notifications
        self.last_text_channel = interaction.channel

        voice_channel = interaction.user.voice.channel

        # Connect to voice channel if not already connected
        if not self.voice_client or not self.voice_client.is_connected():
            try:
                self.voice_client = await voice_channel.connect()
            except Exception as e:
                await interaction.followup.send(f"❌ Failed to connect to voice channel: {e}")
                return
        elif self.voice_client.channel != voice_channel:
            await self.voice_client.move_to(voice_channel)

        # Stream audio in real-time
        try:
            # Get streaming URL from YouTube streamer
            stream_url = await youtube_streamer.get_stream_url(song.url)

            if not stream_url:
                await interaction.followup.send("❌ Failed to get streaming URL")
                return

            # Stream audio using YouTube streamer
            success = await youtube_streamer.stream_audio(self.voice_client, stream_url, lambda e: self._after_playing(e))

            if success:
                # Add current song to history if there was one
                if self.current_song:
                    self.history.append(self.current_song)

                self.current_song = song
                self.is_playing = True
                await interaction.followup.send(f"🎵 Now streaming: **{song.title}**")
            else:
                await interaction.followup.send("❌ Failed to start audio stream")

        except Exception as e:
            print(f"Error streaming song: {e}")
            await interaction.followup.send(f"❌ Error streaming song: {str(e)}")

    def _after_playing(self, error=None):
        """Called when audio finishes playing"""
        if error:
            print(f"Playback error: {error}")

        # Add current song to history if it exists
        if self.current_song:
            self.history.append(self.current_song)

        self.is_playing = False
        self.current_song = None

        # Auto-play next song in queue if available
        # Note: This is called from Discord's voice client, which runs in a separate thread
        # We can't directly send messages here, but we can prepare for the next song
        print(f"Queue has {len(self.queue)} songs remaining")

        # Check if we should leave the channel after song ends
        self._schedule_leave_check()

    async def add_to_queue(self, song):
        """Add a song to the queue"""
        self.queue.append(song)

    def clear_queue(self):
        """Clear the music queue"""
        self.queue.clear()

    def get_queue_info(self):
        """Get information about the current queue"""
        return {
            'current': self.current_song,
            'queue': list(self.queue),
            'is_playing': self.is_playing
        }

    def set_volume(self, volume_level):
        """Set the playback volume (0-100)"""
        # Clamp volume between 0 and 100
        self.volume = max(0, min(100, volume_level))

        # If currently playing, adjust volume
        if self.voice_client and self.voice_client.is_playing():
            # Discord.py doesn't have direct volume control, but we can adjust FFmpeg volume
            # This would require restarting the stream with new volume, which is complex
            # For now, we'll just store the volume for future songs
            pass

        return self.volume

    def pause(self):
        """Pause the current playback"""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            self.is_playing = False
            return True
        return False

    def resume(self):
        """Resume playback"""
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            self.is_playing = True
            return True
        return False

    def _schedule_leave_check(self):
        """Schedule a check to see if bot should leave the channel"""
        # This will be called from a separate thread, so we need to handle it carefully
        # We'll set a flag that the main bot can check
        self._should_check_leave = True

    def should_check_leave(self):
        """Check if we should verify if bot should leave"""
        if hasattr(self, '_should_check_leave') and self._should_check_leave:
            self._should_check_leave = False
            return True
        return False

    async def check_and_leave_if_empty(self, interaction=None, immediate_check=False):
        """Check if the bot should leave the voice channel and leave if empty"""
        if not self.voice_client or not self.voice_client.is_connected():
            return

        # Count non-bot members in the voice channel
        channel = self.voice_client.channel
        human_members = [member for member in channel.members if not member.bot]

        # If no humans left in the channel
        if len(human_members) == 0:
            if immediate_check:
                # Immediate check - leave right away
                print(f"No users in voice channel {channel.name}. Leaving immediately.")
                await self.voice_client.disconnect()
                self.voice_client = None
                self.is_playing = False
                self.current_song = None
                self.queue.clear()

                # Send notification message
                await self._send_leave_notification(channel.name, "all users left")

                if interaction:
                    try:
                        await interaction.followup.send("👋 Left voice channel (no users remaining)")
                    except:
                        pass  # Interaction might be expired
            else:
                # Delayed check - wait 30 seconds to allow users to rejoin
                print(f"No users in voice channel {channel.name}. Leaving in 30 seconds...")

                # Wait 30 seconds to allow users to rejoin
                await asyncio.sleep(30)

                # Check again in case someone rejoined
                human_members = [member for member in channel.members if not member.bot]
                if len(human_members) == 0:
                    print(f"Still no users in voice channel. Leaving now.")
                    await self.voice_client.disconnect()
                    self.voice_client = None
                    self.is_playing = False
                    self.current_song = None
                    self.queue.clear()

                    # Send notification message
                    await self._send_leave_notification(channel.name, "channel remained empty")

                    if interaction:
                        try:
                            await interaction.followup.send("👋 Left voice channel (no users remaining)")
                        except:
                            pass  # Interaction might be expired

    async def play_previous(self, interaction):
        """Play the previous song from history"""
        if not self.history:
            await interaction.followup.send("❌ No previous song to play!")
            return False

        # Get the last song from history
        previous_song = self.history.pop()

        # Add current song to history if exists
        if self.current_song:
            self.history.append(self.current_song)

        # Play the previous song
        await self.stream_and_play(interaction, previous_song)
        return True

    async def _send_leave_notification(self, voice_channel_name, reason):
        """Send a notification message when the bot leaves due to empty channel"""
        if not self.last_text_channel:
            return

        try:
            embed = discord.Embed(
                title="🎵 Music Stopped - No One in Voice Channel",
                description=f"I automatically left **{voice_channel_name}** because {reason}.\n\n"
                           f"**Music stopped** and **queue cleared** to save server resources.",
                color=discord.Color.orange()
            )

            await self.last_text_channel.send(embed=embed)
        except Exception as e:
            print(f"Failed to send leave notification: {e}")

# Create global music player instance
music_player = MusicPlayer()