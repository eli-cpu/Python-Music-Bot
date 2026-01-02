import discord

async def leave_command(interaction: discord.Interaction, music_player):
    """Make the bot leave the voice channel"""
    if not music_player.voice_client or not music_player.voice_client.is_connected():
        await interaction.response.send_message("❌ I'm not connected to any voice channel!")
        return

    await music_player.voice_client.disconnect()
    music_player.voice_client = None
    music_player.is_playing = False
    music_player.current_song = None

    await interaction.response.send_message("👋 Left the voice channel")

def setup_command(bot, music_player):
    """Setup the leave command"""

    @bot.tree.command(name="leave", description="Make the bot leave the voice channel")
    async def leave(interaction: discord.Interaction):
        await leave_command(interaction, music_player)