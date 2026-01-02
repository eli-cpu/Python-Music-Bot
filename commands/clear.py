import discord

async def clear_command(interaction: discord.Interaction, music_player):
    """Clear the music queue"""
    queue_info = music_player.get_queue_info()
    queue_length = len(queue_info['queue'])

    if queue_length == 0:
        await interaction.response.send_message("🗑️ Queue is already empty!")
        return

    music_player.clear_queue()

    embed = discord.Embed(
        title="🗑️ Queue Cleared",
        description=f"Removed {queue_length} song(s) from the queue",
        color=discord.Color.red()
    )

    await interaction.response.send_message(embed=embed)

def setup_command(bot, music_player):
    """Setup the clear command"""

    @bot.tree.command(name="clear", description="Clear the music queue")
    async def clear(interaction: discord.Interaction):
        await clear_command(interaction, music_player)