#!/usr/bin/env python3
"""
Test to verify that slash commands are properly registered before bot.tree.sync()
This test validates the fix for the issue where commands weren't appearing in Discord.
"""

import os
import sys
import unittest

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands
from commands import setup_commands
from utils.streaming_spotify import MusicPlayer


class TestCommandRegistration(unittest.TestCase):
    """Test that commands are properly registered to the bot tree"""

    def setUp(self):
        """Set up test fixtures"""
        # Create bot with necessary intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        # Create music player
        self.music_player = MusicPlayer()

    def test_commands_loaded_before_sync(self):
        """Test that all commands are loaded into bot.tree"""
        print("🧪 Testing that commands are loaded into bot.tree...")
        
        # Setup commands (this is what happens in bot.py now)
        command_count = setup_commands(self.bot, self.music_player)
        
        # Verify commands were loaded
        self.assertGreater(command_count, 0, "No commands were loaded")
        self.assertEqual(command_count, 12, f"Expected 12 commands, got {command_count}")
        
        # Verify commands are in the tree
        tree_commands = self.bot.tree.get_commands()
        self.assertEqual(len(tree_commands), 12, 
                        f"Expected 12 commands in tree, got {len(tree_commands)}")
        
        print(f"✅ All {command_count} commands successfully loaded into bot.tree")

    def test_all_expected_commands_present(self):
        """Test that all expected command names are registered"""
        print("🧪 Testing that all expected commands are present...")
        
        # Setup commands
        setup_commands(self.bot, self.music_player)
        
        # Expected command names
        expected_commands = {
            'play', 'pause', 'resume', 'skip', 'stop', 'backward',
            'join', 'leave', 'volume', 'nowplaying', 'queue', 'clear'
        }
        
        # Get actual command names
        tree_commands = self.bot.tree.get_commands()
        actual_commands = {cmd.name for cmd in tree_commands}
        
        # Verify all expected commands are present
        self.assertEqual(expected_commands, actual_commands,
                        f"Command mismatch. Expected: {expected_commands}, Got: {actual_commands}")
        
        print(f"✅ All expected commands are registered: {', '.join(sorted(actual_commands))}")

    def test_commands_have_descriptions(self):
        """Test that all commands have descriptions"""
        print("🧪 Testing that all commands have descriptions...")
        
        # Setup commands
        setup_commands(self.bot, self.music_player)
        
        # Get commands
        tree_commands = self.bot.tree.get_commands()
        
        # Verify each command has a description
        for cmd in tree_commands:
            self.assertIsNotNone(cmd.description, 
                               f"Command '{cmd.name}' has no description")
            self.assertGreater(len(cmd.description), 0,
                             f"Command '{cmd.name}' has empty description")
            print(f"   /{cmd.name}: {cmd.description}")
        
        print("✅ All commands have valid descriptions")

    def test_command_loading_order(self):
        """Test that commands can be loaded before bot starts (module-level)"""
        print("🧪 Testing command loading order (simulating bot.py)...")
        
        # This simulates what happens in bot.py:
        # 1. Create bot instance
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        bot = commands.Bot(command_prefix='!', intents=intents)
        
        # 2. Create music player
        music_player = MusicPlayer()
        
        # 3. Setup commands BEFORE on_ready would be called
        command_count = setup_commands(bot, music_player)
        
        # 4. Verify commands are in tree (ready for sync)
        tree_commands = bot.tree.get_commands()
        self.assertEqual(len(tree_commands), command_count,
                        "Commands in tree don't match loaded count")
        
        # This demonstrates that commands can be loaded at module level
        # and will be present when bot.tree.sync() is called in on_ready
        print(f"✅ Command loading order is correct: {command_count} commands ready for sync")


def main():
    """Run command registration tests"""
    print("🎵 Command Registration Test Suite")
    print("=" * 60)
    print("Testing the fix for slash commands not appearing in Discord")
    print("=" * 60 + "\n")
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestCommandRegistration('test_commands_loaded_before_sync'))
    suite.addTest(TestCommandRegistration('test_all_expected_commands_present'))
    suite.addTest(TestCommandRegistration('test_commands_have_descriptions'))
    suite.addTest(TestCommandRegistration('test_command_loading_order'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 All command registration tests passed!")
        print("\n✅ The fix is working correctly:")
        print("   - Commands are loaded into bot.tree before bot starts")
        print("   - bot.tree.sync() will now register all 12 commands with Discord")
        print("   - Users will see slash commands when typing / in Discord")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
