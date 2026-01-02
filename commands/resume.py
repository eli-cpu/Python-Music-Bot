import discord

async def resume_command(interaction: discord.Interaction, music_player):
    """Resume playback"""
    if not music_player.voice_client:
        await interaction.response.send_message("❌ I'm not connected to a voice channel!")
        return

    if not music_player.voice_client.is_paused():
        await interaction.response.send_message("▶️ Playback is not paused!")
        return

    success = music_player.resume()
    if success:
        embed = discord.Embed(
            title="▶️ Playback Resumed",
            description=f"Resumed: **{music_player.current_song.title}**",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("❌ Failed to resume playback!")

def setup_command(bot, music_player):
    """Setup the resume command"""

    @bot.tree.command(name="resume", description="Resume playback")
    async def resume(interaction: discord.Interaction):
        await resume_command(interaction, music_player)