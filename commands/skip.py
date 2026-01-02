import discord

async def skip_command(interaction: discord.Interaction, music_player):
    """Skip the current song"""
    if not music_player.voice_client or not music_player.voice_client.is_playing:
        await interaction.response.send_message("❌ No song is currently playing!")
        return

    # Check if there's a next song in queue
    if music_player.queue:
        next_song = music_player.queue.popleft()

        # Stop current song
        music_player.voice_client.stop()
        music_player.is_playing = False
        music_player.current_song = None

        # Play next song
        await music_player.stream_and_play(interaction, next_song)

        embed = discord.Embed(
            title="⏭️ Skipped to Next Song",
            description=f"Now playing: **{next_song.title}**",
            color=discord.Color.blue()
        )
    else:
        # No next song, just stop
        music_player.voice_client.stop()
        music_player.is_playing = False
        music_player.current_song = None

        embed = discord.Embed(
            title="⏭️ Skipped",
            description="No more songs in queue",
            color=discord.Color.orange()
        )

    await interaction.response.send_message(embed=embed)

def setup_command(bot, music_player):
    """Setup the skip command"""

    @bot.tree.command(name="skip", description="Skip the current song")
    async def skip(interaction: discord.Interaction):
        await skip_command(interaction, music_player)