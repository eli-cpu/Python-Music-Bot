import discord
from utils.streaming_spotify import Song

async def play_command(interaction: discord.Interaction, query: str, music_player):
    """Play music from Spotify URL, YouTube URL, or search query"""
    await interaction.response.defer()

    # Store the text channel for future notifications
    music_player.last_text_channel = interaction.channel

    # Check if it's a Spotify URL
    if 'spotify.com' in query:
        spotify_info = music_player.extract_spotify_info(query)
        if spotify_info:
            search_query = spotify_info['query']
            await interaction.followup.send(f"🔍 Searching YouTube for: **{spotify_info['title']}** by **{spotify_info['artist']}**")
        else:
            await interaction.followup.send("❌ Invalid Spotify URL or failed to extract track information")
            return
    else:
        search_query = query

    # Search YouTube
    video_info = await music_player.search_youtube(search_query)

    if not video_info:
        await interaction.followup.send("❌ No results found for your search")
        return

    # Create song object
    song = Song(
        title=video_info['title'],
        url=video_info['url'],
        duration=video_info['duration'],
        thumbnail=video_info.get('thumbnail'),
        requester=interaction.user
    )

    # If not playing anything, play immediately. Otherwise add to queue
    if not music_player.is_playing:
        # Play the song
        await music_player.stream_and_play(interaction, song)
    else:
        # Add to queue
        music_player.queue.append(song)
        embed = discord.Embed(
            title="➕ Added to Queue",
            description=f"**{song.title}**\nPosition: {len(music_player.queue)}",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

def setup_command(bot, music_player):
    """Setup the play command"""

    @bot.tree.command(name="play", description="Play music from Spotify URL, YouTube URL, or search query")
    async def play(interaction: discord.Interaction, query: str):
        await play_command(interaction, query, music_player)