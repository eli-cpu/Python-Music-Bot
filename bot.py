import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from utils.streaming_spotify import MusicPlayer
from commands import setup_commands

# Load environment variables
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.voice_states = True  # Enable voice state intent for music functionality

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Create the music player instance
music_player = MusicPlayer()

# Setup all commands from the commands folder BEFORE bot starts
command_count = setup_commands(bot, music_player)

async def leave_check_loop():
    """Background task to check if bot should leave empty voice channels"""
    while True:
        try:
            # Check every 30 seconds
            await asyncio.sleep(30)

            # Check if music player needs to verify leaving
            if music_player.should_check_leave():
                # Check if bot should leave empty channels
                await music_player.check_and_leave_if_empty()

        except Exception as e:
            print(f"Error in leave check loop: {e}")
            await asyncio.sleep(5)  # Wait a bit before retrying

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} server(s)')

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    # Start the leave check loop
    bot.loop.create_task(leave_check_loop())

@bot.event
async def on_voice_state_update(member, before, after):
    """Called when a user's voice state changes (join/leave/mute/etc.)"""
    # Only check if someone left a voice channel
    if before.channel is not None and after.channel is None:
        # Someone left a voice channel
        if music_player.voice_client and music_player.voice_client.is_connected():
            # Check if the bot's channel is now empty (except for bots)
            channel = music_player.voice_client.channel
            human_members = [m for m in channel.members if not m.bot]

            # If no humans left, leave immediately
            if len(human_members) == 0:
                print(f"All users left voice channel {channel.name}. Leaving immediately.")
                await music_player.check_and_leave_if_empty(immediate_check=True)

# Run the bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in environment variables!")
    print("Please create a .env file with your bot token.")