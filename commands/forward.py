import discord

async def forward_command(interaction: discord.Interaction, music_player):
    """Seek forward 10 seconds in current song"""
    await interaction.response.defer()

    success = await music_player.seek_forward(interaction, 10)
    if not success:
        # If seeking failed, the method already sent an error message
        return

def setup_command(bot, music_player):
    """Setup the forward command"""

    @bot.tree.command(name="forward", description="Seek forward 10 seconds in the current song")
    async def forward(interaction: discord.Interaction):
        await forward_command(interaction, music_player)