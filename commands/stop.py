import discord

async def stop_command(interaction: discord.Interaction, music_player):
    """Stop playback and clear the queue"""
    if not music_player.voice_client:
        await interaction.response.send_message("❌ Not connected to a voice channel!")
        return

    music_player.voice_client.stop()
    music_player.is_playing = False
    music_player.current_song = None
    music_player.queue.clear()

    await interaction.response.send_message("🛑 Stopped playback and cleared the queue!")

def setup_command(bot, music_player):
    """Setup the stop command"""

    @bot.tree.command(name="stop", description="Stop playback and clear the queue")
    async def stop(interaction: discord.Interaction):
        await stop_command(interaction, music_player)