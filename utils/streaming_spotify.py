import os
import asyncio
import time
import re
import discord
from collections import deque

# Import YouTube streamer
from .streaming_youtube import youtube_streamer

# Spotify credentials (optional - no longer required for basic Spotify URL support)
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
        self.current_position = 0  # Current playback position in seconds
        self.playback_start_time = None  # When current playback started (for position tracking)
        self.is_seeking = False  # Flag to prevent _after_playing from resetting song during seeks

    def format_time(self, seconds):
        """Format seconds into HH:MM:SS or MM:SS format"""
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"

    def get_current_position(self):
        """Get the current playback position including elapsed time"""
        if not self.is_playing or self.playback_start_time is None:
            return self.current_position

        # Calculate elapsed time since playback started
        elapsed = time.time() - self.playback_start_time
        return self.current_position + elapsed
        self.last_text_channel = None  # Store last text channel for notifications

        # Initialize Spotify client (optional - for enhanced features)
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            try:
                import spotipy
                from spotipy.oauth2 import SpotifyClientCredentials

                client_credentials_manager = SpotifyClientCredentials(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET
                )
                self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                print("Spotify API client initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize Spotify client: {e}")
                self.spotify = None
        else:
            print("Spotify API credentials not found. Using oEmbed fallback for Spotify URLs.")
            self.spotify = None

    async def extract_spotify_info(self, url):
        """Extract track information from Spotify URL using oEmbed (no API key required)"""
        # Extract track ID from Spotify URL
        match = re.search(r'spotify\.com/track/([a-zA-Z0-9]+)', url)
        if not match:
            return None

        try:
            # Use Spotify's oEmbed endpoint (no API key required)
            import aiohttp

            oembed_url = f"https://open.spotify.com/oembed?url={url}"

            async with aiohttp.ClientSession() as session:
                async with session.get(oembed_url) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Extract title from oEmbed data
                        title_text = data.get('title', '')

                        if not title_text:
                            return None

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

    async def search_youtube(self, query):
        """Search YouTube and return video info using the YouTube streamer"""
        return await youtube_streamer.search_youtube(query)

    async def stream_and_play(self, interaction, song, start_time=0):
        """Stream and play a song from a specific start time"""
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
            success = await youtube_streamer.stream_audio(self.voice_client, stream_url, lambda e: self._after_playing(e), start_time)

            if success:
                # Add current song to history if there was one
                if self.current_song:
                    self.history.append(self.current_song)

                self.current_song = song
                self.is_playing = True
                self.current_position = start_time
                self.playback_start_time = time.time() if start_time == 0 else None
                await interaction.followup.send(f"🎵 Now streaming: **{song.title}**")

                # Auto-send control panel when song starts
                asyncio.create_task(self._send_control_panel())
            else:
                await interaction.followup.send("❌ Failed to start audio stream")

        except Exception as e:
            print(f"Error streaming song: {e}")
            await interaction.followup.send(f"❌ Error streaming song: {str(e)}")

    def _after_playing(self, error=None):
        """Called when audio finishes playing"""
        if error:
            print(f"Playback error: {error}")

            # Check if this is a recoverable network error and we're not seeking
            if not self.is_seeking and self.current_song and self.voice_client and self.voice_client.is_connected():
                # Attempt to recover from stream failure
                asyncio.create_task(self._attempt_stream_recovery(error))
                return  # Don't reset state yet, recovery might succeed

        # Add current song to history if it exists and we're not seeking
        if self.current_song and not self.is_seeking:
            self.history.append(self.current_song)

        self.is_playing = False
        self.playback_start_time = None  # Reset playback timing

        # Only reset current_song if we're not seeking (seeking handles its own state)
        if not self.is_seeking:
            self.current_song = None

        # Auto-play next song in queue if available
        # Note: This is called from Discord's voice client, which runs in a separate thread
        # We can't directly send messages here, but we can prepare for the next song
        print(f"Queue has {len(self.queue)} songs remaining")

        # Check if we should leave the channel after song ends
        self._schedule_leave_check()

        # Auto-send control panel when song finishes (for next song)
        asyncio.create_task(self._send_control_panel())

    async def _send_control_panel(self):
        """Send the music control panel to the last text channel"""
        try:
            if not self.last_text_channel:
                return

            # Import here to avoid circular imports
            from commands.control import MusicControlView

            # Create the control view
            view = MusicControlView(self)

            # Update play/pause button based on current state
            if not self.is_playing and self.current_song:
                # Currently paused
                view.play_pause.label = "▶️ Resume"
                view.play_pause.emoji = "▶️"

            # Create embed with current status
            embed = discord.Embed(
                title="🎵 Music Control Panel",
                description="Use the buttons below to control music playback!",
                color=discord.Color.blue()
            )

            # Add current song info
            if self.current_song:
                status = "▶️ Playing" if self.is_playing else "⏸️ Paused"
                embed.add_field(
                    name=f"{status}: {self.current_song.title}",
                    value=f"Requested by: {self.current_song.requester.mention}",
                    inline=False
                )

            # Add queue info
            queue_info = self.get_queue_info()
            if queue_info['queue']:
                queue_text = f"**{len(queue_info['queue'])}** song(s) in queue"
                if len(queue_info['queue']) <= 3:
                    queue_text += "\n" + "\n".join([f"• {song.title}" for song in queue_info['queue'][:3]])
                embed.add_field(
                    name="📋 Queue",
                    value=queue_text,
                    inline=False
                )
            else:
                embed.add_field(
                    name="📋 Queue",
                    value="Empty",
                    inline=False
                )

            embed.set_footer(text="Click buttons to control music • Panel auto-updates")

            # Send the control panel
            await self.last_text_channel.send(embed=embed, view=view)

        except Exception as e:
            print(f"Error sending control panel: {e}")

    async def _attempt_stream_recovery(self, error):
        """Attempt to recover from a stream failure by refreshing the URL and restarting"""
        try:
            print("Attempting to recover from stream failure...")

            # Wait a moment before attempting recovery
            await asyncio.sleep(1)

            # Check if we still have a valid song and voice connection
            if not self.current_song or not self.voice_client or not self.voice_client.is_connected():
                print("Cannot recover stream: missing song or voice connection")
                return

            # Get a fresh stream URL (the old one might have expired)
            stream_url = await youtube_streamer.get_stream_url(self.current_song.url)

            if not stream_url:
                print("Failed to get fresh stream URL for recovery")
                return

            # Calculate current position to resume from
            current_pos = self.get_current_position()
            print(f"Attempting to resume from position: {self.format_time(current_pos)}")

            # Try to restart the stream from current position
            success = await youtube_streamer.stream_audio(
                self.voice_client,
                stream_url,
                lambda e: self._after_playing(e),
                current_pos
            )

            if success:
                print("Successfully recovered from stream failure!")
                self.is_playing = True
                self.playback_start_time = time.time()
                # Don't reset current_position since we're resuming from it
            else:
                print("Stream recovery failed, resetting song state")
                self.current_song = None
                self.is_playing = False

        except Exception as e:
            print(f"Error during stream recovery: {e}")
            # Ensure we reset state on recovery failure
            self.current_song = None
            self.is_playing = False

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
            # Update current position to include elapsed time before pausing
            if self.playback_start_time is not None:
                self.current_position = self.get_current_position()
                self.playback_start_time = None
            self.is_playing = False
            return True
        return False

    def resume(self):
        """Resume playback"""
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            self.is_playing = True
            # Reset playback start time for position tracking
            self.playback_start_time = time.time()
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

    async def seek_forward(self, interaction, seconds=10):
        """Seek forward by specified seconds in current song"""
        # Comprehensive validation of current state
        if not self.voice_client or not self.voice_client.is_connected():
            await interaction.followup.send("❌ Not connected to a voice channel!", ephemeral=True)
            return False

        if not self.current_song:
            await interaction.followup.send("❌ No song is currently playing!", ephemeral=True)
            return False

        if not hasattr(self.current_song, 'url') or not self.current_song.url:
            await interaction.followup.send("❌ Current song data is corrupted. Please play a new song.", ephemeral=True)
            return False

        # Double-check: ensure we're actually playing
        if not self.is_playing:
            await interaction.followup.send("❌ Music is not currently playing. Use /resume or play a new song.", ephemeral=True)
            return False

        new_position = self.get_current_position() + seconds

        # Don't seek beyond the song duration
        if self.current_song.duration and new_position >= self.current_song.duration:
            # Skip to next song instead
            await self._skip_song(interaction)
            return True

        # Update position and restart stream
        print(f"Attempting to seek forward: current_song={self.current_song is not None}, is_playing={self.is_playing}, voice_connected={self.voice_client.is_connected() if self.voice_client else False}")
        try:
            # Set seeking flag to prevent _after_playing from resetting song state
            self.is_seeking = True

            # Stop current playback first
            if self.voice_client.is_playing():
                self.voice_client.stop()

            # Small delay to ensure clean stop
            await asyncio.sleep(0.1)

            # Start new stream from position
            await self._start_stream_from_position(self.current_song, new_position)
            await interaction.followup.send(f"⏭️ Seeked forward {seconds} seconds (now at {self.format_time(new_position)})", ephemeral=True)
            return True
        except Exception as e:
            print(f"Error seeking forward: {e}")
            await interaction.followup.send("❌ Failed to seek forward!", ephemeral=True)
            return False
        finally:
            # Always reset the seeking flag
            self.is_seeking = False

    async def seek_backward(self, interaction, seconds=10):
        """Seek backward by specified seconds in current song"""
        # Comprehensive validation of current state
        if not self.voice_client or not self.voice_client.is_connected():
            await interaction.followup.send("❌ Not connected to a voice channel!", ephemeral=True)
            return False

        if not self.current_song:
            await interaction.followup.send("❌ No song is currently playing!", ephemeral=True)
            return False

        if not hasattr(self.current_song, 'url') or not self.current_song.url:
            await interaction.followup.send("❌ Current song data is corrupted. Please play a new song.", ephemeral=True)
            return False

        # Double-check: ensure we're actually playing
        if not self.is_playing:
            await interaction.followup.send("❌ Music is not currently playing. Use /resume or play a new song.", ephemeral=True)
            return False

        new_position = max(0, self.get_current_position() - seconds)

        # Update position and restart stream
        try:
            # Set seeking flag to prevent _after_playing from resetting song state
            self.is_seeking = True

            # Stop current playback first
            if self.voice_client.is_playing():
                self.voice_client.stop()

            # Small delay to ensure clean stop
            await asyncio.sleep(0.1)

            # Start new stream from position
            await self._start_stream_from_position(self.current_song, new_position)
            await interaction.followup.send(f"⏮️ Seeked backward {seconds} seconds (now at {self.format_time(new_position)})", ephemeral=True)
            return True
        except Exception as e:
            print(f"Error seeking backward: {e}")
            await interaction.followup.send("❌ Failed to seek backward!", ephemeral=True)
            return False
        finally:
            # Always reset the seeking flag
            self.is_seeking = False

    async def _start_stream_from_position(self, song, start_time):
        """Start streaming a song from a specific position"""
        # Triple validation
        if not song:
            raise Exception("Song object is None")
        if not hasattr(song, 'url'):
            raise Exception("Song object missing 'url' attribute")
        if not song.url or not isinstance(song.url, str) or song.url.strip() == "":
            raise Exception("Song URL is empty or invalid")

        try:
            # Get streaming URL from YouTube streamer
            stream_url = await youtube_streamer.get_stream_url(song.url)

            if not stream_url:
                raise Exception("Failed to get stream URL from YouTube")

            # Stream audio using YouTube streamer from position
            success = await youtube_streamer.stream_audio(self.voice_client, stream_url, lambda e: self._after_playing(e), start_time)

            if success:
                self.current_song = song
                self.is_playing = True
                self.current_position = start_time
                self.playback_start_time = time.time()
                print(f"Successfully started streaming: {song.title if hasattr(song, 'title') else 'Unknown'} from {self.format_time(start_time)}")
            else:
                raise Exception("Failed to start audio stream")

        except Exception as e:
            print(f"Error starting stream from position: {e}")
            # Reset state on failure
            self.is_playing = False
            if not self.is_seeking:  # Don't reset song during seeks
                self.current_song = None
            raise

    async def _skip_song(self, interaction):
        """Helper method to skip to next song (used internally)"""
        if not self.queue:
            await interaction.followup.send("❌ No more songs in queue!", ephemeral=True)
            return

        next_song = self.queue.popleft()

        # Stop current song
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()

        # Play next song
        await self.stream_and_play(interaction, next_song)
        await interaction.followup.send(f"⏭️ Skipped! Now playing: **{next_song.title}**", ephemeral=True)

# Create global music player instance
music_player = MusicPlayer()