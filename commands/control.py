import discord
from discord import ui
from utils.streaming_spotify import Song

class MusicControlView(ui.View):
    """Interactive control panel for music bot"""

    def __init__(self, music_player, timeout=300):  # 5 minute timeout
        super().__init__(timeout=timeout)
        self.music_player = music_player

        # Add GitHub link button
        github_button = ui.Button(
            label="🔗 GitHub",
            style=discord.ButtonStyle.link,
            url="https://github.com/eli-cpu",
            emoji="🔗",
            row=3
        )
        self.add_item(github_button)

    async def _skip_song(self, interaction):
        """Helper method to skip to next song"""
        await interaction.response.defer(ephemeral=True)

        if not self.music_player.voice_client or not self.music_player.voice_client.is_playing:
            await interaction.followup.send("❌ No song is currently playing!", ephemeral=True)
            return

        # Check if there's a next song in queue
        if self.music_player.queue:
            next_song = self.music_player.queue.popleft()

            # Stop current song
            self.music_player.voice_client.stop()
            self.music_player.is_playing = False
            self.music_player.current_song = None

            # Play next song
            await self.music_player.stream_and_play(interaction, next_song)
            await interaction.followup.send(f"⏭️ Skipped! Now playing: **{next_song.title}**", ephemeral=True)
        else:
            # No next song, just stop
            self.music_player.voice_client.stop()
            self.music_player.is_playing = False
            self.music_player.current_song = None
            await interaction.followup.send("⏭️ Skipped! No more songs in queue.", ephemeral=True)

    async def _go_back(self, interaction):
        """Helper method to go back to previous song"""
        await interaction.response.defer(ephemeral=True)

        if not self.music_player.history:
            await interaction.followup.send("❌ No previous song to play!", ephemeral=True)
            return

        if not self.music_player.voice_client:
            await interaction.followup.send("❌ I'm not connected to a voice channel!", ephemeral=True)
            return

        success = await self.music_player.play_previous(interaction)
        if success:
            await interaction.followup.send(f"⏮️ Playing previous song: **{self.music_player.current_song.title}**", ephemeral=True)

    @ui.button(label="⏯️ Play/Pause", style=discord.ButtonStyle.primary, emoji="⏯️", row=0)
    async def play_pause(self, interaction: discord.Interaction, button: ui.Button):
        """Toggle play/pause"""
        await interaction.response.defer(ephemeral=True)

        if not self.music_player.voice_client:
            await interaction.followup.send("❌ I'm not connected to a voice channel!", ephemeral=True)
            return

        if self.music_player.is_playing:
            # Currently playing, so pause
            success = self.music_player.pause()
            if success:
                button.label = "▶️ Resume"
                button.emoji = "▶️"
                await interaction.edit_original_response(view=self)
                await interaction.followup.send("⏸️ Music paused!", ephemeral=True)
            else:
                await interaction.followup.send("❌ Failed to pause!", ephemeral=True)
        else:
            # Currently paused, so resume
            success = self.music_player.resume()
            if success:
                button.label = "⏯️ Play/Pause"
                button.emoji = "⏯️"
                await interaction.edit_original_response(view=self)
                await interaction.followup.send("▶️ Music resumed!", ephemeral=True)
            else:
                await interaction.followup.send("❌ Failed to resume!", ephemeral=True)

    @ui.button(label="⏮️ Back", style=discord.ButtonStyle.secondary, emoji="⏮️", row=1)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        """Go back to previous song"""
        await self._go_back(interaction)

    @ui.button(label="⏭️ Skip", style=discord.ButtonStyle.secondary, emoji="⏭️", row=1)
    async def skip(self, interaction: discord.Interaction, button: ui.Button):
        """Skip current song"""
        await self._skip_song(interaction)

    @ui.button(label="⏮️ Backward", style=discord.ButtonStyle.secondary, emoji="⏮️", row=2)
    async def backward_button(self, interaction: discord.Interaction, button: ui.Button):
        """Seek backward 10 seconds in current song"""
        await interaction.response.defer(ephemeral=True)
        await self.music_player.seek_backward(interaction, 10)

    @ui.button(label="⏭️ Forward", style=discord.ButtonStyle.secondary, emoji="⏭️", row=2)
    async def forward(self, interaction: discord.Interaction, button: ui.Button):
        """Seek forward 10 seconds in current song"""
        await interaction.response.defer(ephemeral=True)
        await self.music_player.seek_forward(interaction, 10)

    @ui.button(label="🗑️ Clear", style=discord.ButtonStyle.danger, emoji="🗑️", row=3)
    async def clear(self, interaction: discord.Interaction, button: ui.Button):
        """Clear the music queue"""
        queue_info = self.music_player.get_queue_info()
        queue_length = len(queue_info['queue'])

        if queue_length == 0:
            await interaction.response.send_message("🗑️ Queue is already empty!", ephemeral=True)
            return

        self.music_player.clear_queue()
        await interaction.response.send_message(f"🗑️ Cleared {queue_length} song(s) from queue!", ephemeral=True)

async def control_command(interaction: discord.Interaction, music_player):
    """Show the music control panel"""
    # Store the text channel for notifications
    music_player.last_text_channel = interaction.channel

    # Create the control view
    view = MusicControlView(music_player)

    # Update play/pause button based on current state
    if not music_player.is_playing and music_player.current_song:
        # Currently paused
        view.play_pause.label = "▶️ Resume"
        view.play_pause.emoji = "▶️"

    # Create compact embed with current status above buttons
    embed = discord.Embed(
        color=discord.Color.blue()
    )

    # Add current song info
    if music_player.current_song:
        status = "▶️ Playing" if music_player.is_playing else "⏸️ Paused"
        embed.add_field(
            name="🎵 Current Song",
            value=f"{status} **{music_player.current_song.title}**\nRequested by: {music_player.current_song.requester.mention}",
            inline=False
        )

    # Add queue info
    queue_info = music_player.get_queue_info()
    if queue_info['queue']:
        queue_text = f"📋 **{len(queue_info['queue'])}** song(s) in queue"
        if len(queue_info['queue']) <= 3:
            queue_text += "\n" + "\n".join([f"• {song.title}" for song in queue_info['queue'][:3]])
        embed.add_field(
            name="‎",  # Invisible character for spacing
            value=queue_text,
            inline=False
        )
    else:
        embed.add_field(
            name="‎",  # Invisible character for spacing
            value="📋 Queue is empty",
            inline=False
        )

    embed.set_footer(text="🎛️ Use the buttons below to control playback")

    await interaction.response.send_message(embed=embed, view=view)

def setup_command(bot, music_player):
    """Setup the control command"""

    @bot.tree.command(name="control", description="Show interactive music control panel with buttons")
    async def control(interaction: discord.Interaction):
        await control_command(interaction, music_player)