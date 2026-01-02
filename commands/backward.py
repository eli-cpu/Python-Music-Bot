import discord

async def backward_command(interaction: discord.Interaction, music_player):
    """Go back to the previous song"""
    await interaction.response.defer()

    if not music_player.history:
        await interaction.followup.send("❌ No previous song to play!")
        return

    if not music_player.voice_client:
        await interaction.followup.send("❌ I'm not connected to a voice channel!")
        return

    success = await music_player.play_previous(interaction)
    if success:
        embed = discord.Embed(
            title="⏮️ Playing Previous Song",
            description=f"Went back to: **{music_player.current_song.title}**",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed)

def setup_command(bot, music_player):
    """Setup the backward command"""

    @bot.tree.command(name="backward", description="Go back to the previous song")
    async def backward(interaction: discord.Interaction):
        await backward_command(interaction, music_player)