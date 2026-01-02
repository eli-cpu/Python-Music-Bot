import discord

async def pause_command(interaction: discord.Interaction, music_player):
    """Pause the current song"""
    if not music_player.voice_client:
        await interaction.response.send_message("❌ I'm not connected to a voice channel!")
        return

    if not music_player.voice_client.is_playing():
        await interaction.response.send_message("❌ No song is currently playing!")
        return

    if music_player.voice_client.is_paused():
        await interaction.response.send_message("⏸️ Playback is already paused!")
        return

    success = music_player.pause()
    if success:
        embed = discord.Embed(
            title="⏸️ Playback Paused",
            description=f"Paused: **{music_player.current_song.title}**",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❌ Failed to pause playback!")

def setup_command(bot, music_player):
    """Setup the pause command"""

    @bot.tree.command(name="pause", description="Pause the current song")
    async def pause(interaction: discord.Interaction):
        await pause_command(interaction, music_player)