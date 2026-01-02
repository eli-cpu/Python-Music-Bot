import discord

async def nowplaying_command(interaction: discord.Interaction, music_player):
    """Show information about the currently playing song"""
    if not music_player.current_song:
        await interaction.response.send_message("🎵 No song is currently playing!")
        return

    song = music_player.current_song
    embed = discord.Embed(
        title="🎵 Now Playing",
        description=f"**{song.title}**",
        color=discord.Color.blue()
    )

    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)

    embed.add_field(name="Duration", value=f"{song.duration // 60}:{song.duration % 60:02d}", inline=True)
    embed.add_field(name="Requested by", value=song.requester.mention, inline=True)

    await interaction.response.send_message(embed=embed)

def setup_command(bot, music_player):
    """Setup the nowplaying command"""

    @bot.tree.command(name="nowplaying", description="Show information about the currently playing song")
    async def nowplaying(interaction: discord.Interaction):
        await nowplaying_command(interaction, music_player)