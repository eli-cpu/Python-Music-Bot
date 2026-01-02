import discord
import os
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

    # Setup all commands from the commands folder
    command_count = setup_commands(bot, music_player)

# Run the bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in environment variables!")
    print("Please create a .env file with your bot token.")