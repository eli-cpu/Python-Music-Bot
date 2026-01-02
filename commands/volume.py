import discord

async def volume_command(interaction: discord.Interaction, level: int, music_player):
    """Set the playback volume"""
    if level < 0 or level > 100:
        await interaction.response.send_message("❌ Volume must be between 0 and 100!")
        return

    old_volume = music_player.volume
    new_volume = music_player.set_volume(level)

    embed = discord.Embed(
        title="🔊 Volume Changed",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Volume Level",
        value=f"{old_volume}% → {new_volume}%",
        inline=False
    )

    if not music_player.voice_client or not music_player.voice_client.is_playing():
        embed.add_field(
            name="Note",
            value="Volume change will apply to the next song played",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

def setup_command(bot, music_player):
    """Setup the volume command"""

    @bot.tree.command(name="volume", description="Set the playback volume (0-100)")
    async def volume(interaction: discord.Interaction, level: int):
        await volume_command(interaction, level, music_player)