import discord

async def backward_command(interaction: discord.Interaction, music_player):
    """Seek backward 10 seconds in current song"""
    await interaction.response.defer()

    success = await music_player.seek_backward(interaction, 10)
    if not success:
        # If seeking failed, the method already sent an error message
        return

def setup_command(bot, music_player):
    """Setup the backward command"""

    @bot.tree.command(name="backward", description="Seek backward 10 seconds in the current song")
    async def backward(interaction: discord.Interaction):
        await backward_command(interaction, music_player)