import discord

async def queue_command(interaction: discord.Interaction, music_player):
    """Show the current music queue"""
    queue_info = music_player.get_queue_info()

    if not queue_info['current'] and not queue_info['queue']:
        await interaction.response.send_message("📋 Queue is empty! Add some songs with `/play`")
        return

    embed = discord.Embed(
        title="🎵 Music Queue",
        color=discord.Color.blue()
    )

    # Current song
    if queue_info['current']:
        song = queue_info['current']
        status = "▶️ Playing" if queue_info['is_playing'] else "⏸️ Paused"
        embed.add_field(
            name=f"{status}: {song.title}",
            value=f"Duration: {song.duration // 60}:{song.duration % 60:02d} | Requested by: {song.requester.mention}",
            inline=False
        )

    # Queue
    if queue_info['queue']:
        queue_text = ""
        for i, song in enumerate(queue_info['queue'][:10], 1):  # Show first 10 songs
            duration = f"{song.duration // 60}:{song.duration % 60:02d}"
            queue_text += f"{i}. **{song.title}** - {duration} - {song.requester.mention}\n"

        if len(queue_info['queue']) > 10:
            queue_text += f"... and {len(queue_info['queue']) - 10} more songs"

        embed.add_field(
            name=f"📋 Up Next ({len(queue_info['queue'])} songs)",
            value=queue_text,
            inline=False
        )
    else:
        embed.add_field(
            name="📋 Up Next",
            value="No songs in queue",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

def setup_command(bot, music_player):
    """Setup the queue command"""

    @bot.tree.command(name="queue", description="Show the current music queue")
    async def queue(interaction: discord.Interaction):
        await queue_command(interaction, music_player)