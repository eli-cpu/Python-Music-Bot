"""
Commands Package

Automatically discovers and imports all command modules from this folder.
Each command should be in its own .py file and define setup_command(bot, music_player) function.
"""

import os
import importlib
import inspect
from pathlib import Path

def setup_commands(bot, music_player):
    """
    Automatically discover and setup all commands from this folder.

    Args:
        bot: The Discord bot instance
        music_player: The MusicPlayer instance to pass to commands
    """
    commands_dir = Path(__file__).parent
    command_count = 0

    # Get all .py files in the commands directory (excluding __init__.py)
    command_files = [
        f for f in commands_dir.glob("*.py")
        if f.name != "__init__.py"
    ]

    for command_file in command_files:
        module_name = command_file.stem  # Remove .py extension

        try:
            # Import the module dynamically
            module = importlib.import_module(f"commands.{module_name}")

            # Check if it has a setup_command function
            if hasattr(module, 'setup_command'):
                setup_func = getattr(module, 'setup_command')

                # Call the setup function with bot and music_player
                setup_func(bot, music_player)
                command_count += 1
                print(f"✅ Loaded command: {module_name}")

            else:
                print(f"⚠️  Skipping {module_name}: no setup_command function found")

        except Exception as e:
            print(f"❌ Failed to load command {module_name}: {e}")

    print(f"🎵 Loaded {command_count} command(s) from commands folder")
    return command_count