import discord

async def join_command(interaction: discord.Interaction, music_player):
    """Make the bot join your voice channel"""
    if not interaction.user.voice:
        await interaction.response.send_message("❌ You must be in a voice channel first!")
        return

    # Store the text channel for future notifications
    music_player.last_text_channel = interaction.channel

    voice_channel = interaction.user.voice.channel

    if music_player.voice_client and music_player.voice_client.is_connected():
        if music_player.voice_client.channel == voice_channel:
            await interaction.response.send_message("✅ I'm already in your voice channel!")
        else:
            await music_player.voice_client.move_to(voice_channel)
            await interaction.response.send_message(f"🔊 Moved to **{voice_channel.name}**")
    else:
        try:
            music_player.voice_client = await voice_channel.connect()
            await interaction.response.send_message(f"🔊 Joined **{voice_channel.name}**")
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to join voice channel: {e}")

def setup_command(bot, music_player):
    """Setup the join command"""

    @bot.tree.command(name="join", description="Make the bot join your voice channel")
    async def join(interaction: discord.Interaction):
        await join_command(interaction, music_player)