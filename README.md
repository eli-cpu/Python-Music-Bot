# Discord Music Bot

A basic Discord bot setup ready for music functionality.

## Setup Instructions

### 1. Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give your bot a name (e.g., "Music Bot")
4. Go to the "Bot" section in the left sidebar
5. Click "Add Bot" to create your bot
6. Copy the bot token (keep this secret!)

### 2. Set up Environment Variables

Create a `.env` file in the project root with your bot credentials:

```
DISCORD_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
```

- Replace `your_bot_token_here` with the bot token from the "Bot" section
- Replace `your_client_id_here` with the Application ID from the "General Information" section
- For Spotify API: Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), create an app, and copy the Client ID and Client Secret

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Important Dependencies:**

- **FFmpeg** (Required for audio processing):

  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)
  - **Linux:** `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora)
  - **macOS:** `brew install ffmpeg`

- **PyNaCl** (Required for Discord voice functionality):
  ```bash
  pip install PyNaCl>=1.5.0
  ```
  **Note:** Without PyNaCl, voice commands like `/join`, `/play`, etc. will fail with connection errors.

### 4. Run the Bot

```bash
python bot.py
```

### 5. Invite the Bot to Your Server

1. In the Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Select the following scopes:
   - `bot`
3. Select the following permissions:
   - Send Messages
   - Use Slash Commands
   - Connect
   - Speak
   - Use Voice Activity
4. Copy the generated URL and paste it into your browser
5. Select your server and authorize the bot

### 6. Verify Setup

Once the bot is running and invited to your server, you should see:

- The bot comes online in your server
- A message in your console: "BotName has connected to Discord!"

## Current Features

- Basic bot setup with Discord connection
- **🎵 Complete Music Bot with Queue System**
- **Real-time music streaming with Spotify integration**
- **🛠️ Stream Recovery System** - Automatically recovers from network interruptions
  - Handles YouTube stream timeouts and connection drops
  - Refreshes expired stream URLs automatically
  - Resumes playback from the correct position after recovery
  - Graceful fallback if recovery fails
- **Modular architecture**:
  - `utils/` package - Music streaming functionality
    - `utils/streaming_spotify.py` - Spotify integration and music player
    - `utils/streaming_youtube.py` - YouTube streaming functionality
  - `commands/` package - Auto-discovered Discord commands (14 commands)
    - Each command in its own file (e.g., `commands/play.py`)
    - Automatic command loading - just add new `.py` files!
- **Queue system** - Add multiple songs, skip, pause/resume, volume control
- **History tracking** - Go back to previous songs
- **Auto-Control Panel** - Interactive UI automatically appears when songs start/change
- **Testing tools** - Run `python test_all.py` to verify functionality

## Music Playback Guide

### `/play` Command Behavior

The `/play` command accepts different types of input and behaves as follows:

#### 🎵 **YouTube URLs** (Works without API keys)

```
/play https://www.youtube.com/watch?v=dQw4w9WgXcQ
/play https://youtu.be/dQw4w9WgXcQ
/play https://music.youtube.com/watch?v=dQw4w9WgXcQ
```

**Result:** ✅ Plays the exact YouTube video directly

#### 🔍 **Search Queries** (Works without API keys)

```
/play never gonna give you up
/play rick astley never gonna give you up
/play favorite song name
```

**Result:** ✅ Searches YouTube and plays the best match

#### 🎼 **Spotify URLs** (Requires Spotify API credentials)

```
/play https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC
/play https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC?si=abc123
```

**Result:**

- ✅ **With Spotify credentials**: Extracts track info, searches YouTube, plays match
- ❌ **Without Spotify credentials**: Shows error message

#### 📝 **What Happens Internally:**

1. **YouTube URL**: Direct streaming from the provided URL
2. **Search Query**: yt-dlp searches YouTube, picks top result, streams it
3. **Spotify URL**:
   - Extracts track title/artist using Spotify API
   - Searches YouTube for "title artist"
   - Streams the best YouTube match

## 🎛️ **All Commands - Fully Implemented:**

### **Music Playback:**

- `/play <query>` - Play music from YouTube, Spotify, or search
- `/skip` - Skip current song and play next in queue
- `/stop` - Stop playback and clear queue
- `/pause` - Pause current song
- `/resume` - Resume paused song
- `/backward` - Play previous song from history

### **Queue Management:**

- `/queue` - Show current queue with song details
- `/clear` - Clear all songs from queue

### **Voice Control:**

- `/join` - Join your voice channel
- `/leave` - Leave voice channel
- `/volume <0-100>` - Set playback volume

### **Information:**

- `/nowplaying` - Show current song with thumbnail
- `/control` - Interactive control panel with clickable buttons

### **Navigation:**

- `/forward` - Seek forward 10 seconds in current song
- `/backward` - Seek backward 10 seconds in current song

## 🎛️ **Interactive Control Panel**

**✨ Auto-Appearing UI**: The control panel automatically appears in the text channel whenever:

- A new song starts playing (`/play`, `/skip`, etc.)
- A song finishes and the next one begins
- The bot recovers from a stream interruption

Use `/control` to manually display an interactive panel with clickable buttons for easy music control:

### **First Row - Playback Controls:**

- **⏯️ Play/Pause** - Toggle between play and pause (button changes dynamically)
- **⏭️ Skip** - Skip to next song in queue
- **⏮️ Back** - Play previous song from history
- **⏭️ Forward** - Seek forward 10 seconds in current song
- **⏮️ Backward** - Seek backward 10 seconds in current song

### **Second Row - Management:**

- **🗑️ Clear** - Clear all songs from queue
- **🔗 GitHub** - Link to project repository

### **Features:**

- ✅ **Real-time updates** - Current song and queue status
- ✅ **Smart buttons** - Play/Pause button changes based on current state
- ✅ **Interactive feedback** - Buttons respond with confirmation messages
- ✅ **Queue display** - Shows upcoming songs in the panel

## 🤖 **Smart Auto-Leave Feature**

The bot automatically leaves voice channels when no users are present and sends helpful notifications:

### **When Music Ends:**

- After a song finishes, if no users are in the voice channel, the bot waits 30 seconds
- If still no users after 30 seconds, the bot automatically leaves and clears the queue
- **Sends a notification** explaining why music stopped

### **When Users Leave:**

- If the last human user leaves the voice channel (while music is playing or not), the bot immediately leaves
- **Sends an immediate notification** about the empty channel
- No waiting period when users actively leave

### **Notification Messages:**

The bot sends clear embed messages in the text channel where music commands were last used:

```
🎵 Music Stopped - No One in Voice Channel

I automatically left [channel name] because [reason].

Music stopped and queue cleared to save server resources.
```

### **Benefits:**

- ✅ **Saves server resources** - Bot doesn't stay in empty channels
- ✅ **Clear communication** - Users know why music stopped
- ✅ **Automatic cleanup** - Queue is cleared when leaving
- ✅ **Smart timing** - Immediate leave when users leave, delayed when music ends
- ✅ **User-friendly** - Helpful notifications explain what happened

### 🎯 **Fully Functional Without API Keys:**

- ✅ YouTube URLs and search queries
- ✅ All voice and queue commands
- ✅ Pause/resume, skip, volume control
- ✅ Queue system with auto-play next
- ✅ Song history and backward functionality

### 🔑 **Optional Enhancement:**

- ✅ Spotify URL support (requires API credentials)

## Testing the Bot

Before running the Discord bot, validate your setup and test all functionality:

### Setup Validation

```bash
python validate_setup.py
```

Validates file structure, syntax, and project organization without requiring dependencies.

### Quick Test Runner

```bash
python test_all.py
```

Runs the complete test suite from the project root (requires installed dependencies).

### Comprehensive Test Suite

```bash
cd tests && python run_tests.py
```

Runs all individual test suites with detailed output.

### Individual Test Suites

#### Core Functionality Tests

```bash
cd tests && python test_streaming.py
```

Tests:

- Spotify URL extraction
- YouTube search functionality
- Stream URL extraction
- Complete Spotify → YouTube → Stream flow

#### Audio Pipeline Tests

```bash
cd tests && python test_audio.py
```

Tests:

- FFmpeg availability and version
- Audio stream processing
- Discord FFmpeg integration
- End-to-end audio pipeline

#### Queue System Tests

```bash
cd tests && python test_queue.py
```

Tests:

- Song class functionality
- Queue operations (add, remove, clear)
- Current song tracking
- Playback state management

#### Discord Bot Tests

```bash
cd tests && python test_discord_bot.py
```

Tests:

- Bot initialization and configuration
- Command structure and registration
- Music player integration
- All bot command functions
- Environment variable handling

  - `/play <spotify_url>` - Stream music from Spotify URL (automatically searches YouTube)
  - `/play <query>` - Stream music from YouTube URL or search query
  - `/skip` - Skip current song
  - `/stop` - Stop playback and clear queue
  - `/nowplaying` - Show current song info with thumbnail
  - `/join` - Join your voice channel
  - `/leave` - Leave voice channel

- **Commands still to be implemented**:
  - `/backward` - Go back to previous song
  - `/pause` - Pause current song
  - `/resume` - Resume playback
  - `/queue` - Show current queue
  - `/volume <level>` - Set volume level
  - `/clear` - Clear the queue

## Troubleshooting

### Common Issues

- **Bot not responding**: Make sure your `.env` file has the correct token
- **Permission errors**: Ensure the bot has proper permissions in your server
- **Connection issues**: Check that your bot token is valid and hasn't expired

### Stream Issues & Recovery

The bot includes an **automatic stream recovery system** that handles common streaming problems:

- **"Connection reset by peer" or TLS errors**: The bot will automatically attempt to refresh the stream URL and resume playback from the correct position
- **Stream timeouts**: If YouTube streams expire (typically after 6+ hours), the bot fetches a fresh URL and continues playing
- **Network interruptions**: Temporary connection issues are handled with automatic retry logic and better FFmpeg buffering

**What happens during recovery:**

1. Stream failure is detected
2. Bot waits 1 second to avoid rapid retries
3. Fetches a fresh stream URL from YouTube
4. Resumes playback from the current position
5. Shows success/failure messages in the console

**If recovery fails:**

- The bot gracefully stops the current song
- Moves to the next song in queue (if available)
- Sends appropriate user notifications

This system ensures uninterrupted music playback even during network issues or long listening sessions.
