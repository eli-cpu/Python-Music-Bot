# Spotify Wrapper - Full-Stack Music Streaming Platform

A comprehensive music streaming platform with Spotify integration, YouTube fallback, ad-blocking, and multiple frontends (Web, Discord Bot, Mobile).

## 🎵 Features

### Core Features
- ✅ **Spotify API Integration** - Full Spotify library access with OAuth authentication
- ✅ **YouTube Fallback** - Automatically searches YouTube when tracks aren't on Spotify
- ✅ **Ad-Blocking** - SponsorBlock integration removes ads and sponsored segments
- ✅ **Multiple Frontends**:
  - Web Application (React)
  - Discord Bot (No login required)
  - Mobile App (React Native)
- ✅ **Vercel Deployment Ready** - Easy deployment to Vercel

### Web Frontend Features
- User authentication with Spotify OAuth
- Search for songs, artists, and albums
- View and play from your Spotify playlists
- Real-time now playing display
- Clean, modern UI with Spotify-inspired design

### Discord Bot Features
- Music playback in voice channels
- Queue management system
- Interactive control panel with buttons
- No authentication required
- 14+ slash commands

### Backend API Features
- RESTful API with Flask
- Automatic YouTube fallback for unavailable tracks
- Session-based authentication
- Protected user endpoints
- Health check monitoring

## 📁 Project Structure

```
Python-Music-Bot/
├── backend/              # Flask REST API
│   ├── app.py           # Main backend application
│   └── requirements.txt
├── frontend/            # React web app
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── App.js
│   │   └── App.css
│   ├── public/
│   └── package.json
├── mobile/              # React Native app
│   ├── src/
│   │   ├── screens/    # App screens
│   │   └── services/   # API integration
│   ├── App.js
│   └── package.json
├── bot.py              # Discord bot (existing)
├── commands/           # Bot commands
├── utils/              # Bot utilities
├── vercel.json         # Vercel deployment config
├── DEPLOYMENT.md       # Detailed deployment guide
└── README.md

```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Spotify Developer Account
- Discord Bot Token (optional, for bot)

### Environment Setup

Create a `.env` file in the project root:

```env
# Discord Bot
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CLIENT_ID=your_discord_client_id

# Spotify API
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/callback

# Backend
FLASK_SECRET_KEY=your_random_secret_key
PORT=5000
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend runs on `http://localhost:5000`

### Web Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

### Discord Bot Setup

```bash
pip install -r requirements.txt
python bot.py
```

### Mobile App Setup

```bash
cd mobile
npm install
npm run android  # or npm run ios
```

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/login` | Initiate Spotify OAuth |
| POST | `/api/auth/callback` | OAuth callback handler |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/status` | Check auth status |

### Music Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search?q={query}` | Search tracks |
| GET | `/api/track/{track_id}` | Get track info |
| POST | `/api/stream` | Get stream URL with fallback |

### User Endpoints (Protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/playlists` | Get user playlists |
| GET | `/api/playlist/{playlist_id}` | Get playlist tracks |
| GET | `/api/user/current-track` | Get now playing |

## 🎮 Discord Bot Commands

The Discord bot runs independently and requires no login:

### Playback Commands
- `/play <query>` - Play from Spotify/YouTube
- `/pause` - Pause playback
- `/resume` - Resume playback
- `/skip` - Skip current track
- `/stop` - Stop and clear queue

### Queue Commands
- `/queue` - Show current queue
- `/clear` - Clear all tracks
- `/nowplaying` - Show current track

### Control Commands
- `/control` - Interactive button panel (✅ Fixed: Removed duplicate icon)
- `/join` - Join voice channel
- `/leave` - Leave voice channel
- `/volume <0-100>` - Set volume

### Navigation
- `/forward` - Seek forward 10s
- `/backward` - Seek backward 10s or play previous track

## 🐛 Bug Fix: Duplicate Icon in Control Panel

**Fixed Issue**: The GitHub button in the Discord bot's control panel had duplicate icons.

**Before:**
```python
label="🔗 GitHub",  # Icon in label
emoji="🔗",         # Duplicate icon
```

**After:**
```python
label="GitHub",     # Clean label
emoji="🔗",        # Single icon
```

This fix ensures a clean, professional appearance in the interactive control panel.

## 🌐 Deployment on Vercel

### Quick Deploy

```bash
# Install Vercel CLI
npm install -g vercel

# Login and deploy
vercel login
vercel

# Production deployment
vercel --prod
```

### Environment Variables

Set these in Vercel dashboard:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI` (update to your domain)
- `FLASK_SECRET_KEY`

### Important Note

⚠️ **Discord Bot on Vercel**: The Discord bot requires a persistent connection and cannot run on Vercel's serverless infrastructure. Deploy the bot separately on:
- Heroku
- Railway
- DigitalOcean
- AWS EC2
- Or keep it running locally

The web frontend and API work perfectly on Vercel.

## 🏗️ Architecture

### Separation of Concerns

1. **Backend API** - Handles Spotify/YouTube integration, authentication
2. **Web Frontend** - User-facing web app with login
3. **Discord Bot** - Independent instance for Discord (no login)
4. **Mobile App** - Native mobile experience

### Key Design Decisions

- **No interaction between Frontend and Bot** - Completely independent
- **Stateless API** - Easy to scale horizontally
- **Session-based auth** - Simple and secure for web
- **No auth for bot** - Better UX for Discord users

## 🔧 Development

### Running All Services

```bash
# Terminal 1: Backend
cd backend && python app.py

# Terminal 2: Frontend
cd frontend && npm start

# Terminal 3: Discord Bot
python bot.py
```

### Testing API

```bash
# Health check
curl http://localhost:5000/api/health

# Search
curl "http://localhost:5000/api/search?q=test"

# Stream with fallback
curl -X POST http://localhost:5000/api/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "never gonna give you up"}'
```

## 🔐 Security

- ✅ Environment variables for secrets
- ✅ Session-based authentication
- ✅ CORS configured properly
- ✅ No credentials in code
- ✅ OAuth flow for Spotify

## 🛠️ Tech Stack

### Backend
- Flask - Web framework
- Spotipy - Spotify API wrapper
- yt-dlp - YouTube integration with ad-blocking
- Flask-CORS - Cross-origin support

### Frontend
- React 18 - UI framework
- React Router - Navigation
- Axios - HTTP client
- CSS3 - Styling

### Mobile
- React Native - Mobile framework
- React Navigation - Mobile navigation
- Axios - HTTP client

### Bot
- discord.py - Discord API
- FFmpeg - Audio processing
- PyNaCl - Voice encryption

## 📖 Additional Documentation

- [DEPLOYMENT.md](./DEPLOYMENT.md) - Comprehensive deployment guide
- [README_ORIGINAL.md](./README_ORIGINAL.md) - Original Discord bot documentation

## 🐛 Troubleshooting

### Backend Issues
- **ImportError**: Run `pip install -r backend/requirements.txt`
- **Spotify API fails**: Check credentials in `.env`
- **CORS errors**: Ensure frontend URL is in CORS config

### Frontend Issues
- **Blank page**: Check backend is running
- **Login fails**: Verify Spotify redirect URI
- **Build fails**: Delete `node_modules`, run `npm install`

### Bot Issues
- **Not responding**: Check Discord token
- **Voice fails**: Install PyNaCl and FFmpeg
- **Music skips**: Check network connection

## 🎯 Future Enhancements

- [ ] Lyrics integration
- [ ] Social features (share playlists)
- [ ] Collaborative playlists
- [ ] Audio visualization
- [ ] Podcast support
- [ ] Offline downloads
- [ ] Cross-device sync
- [ ] Advanced queue management

## 📄 License

See LICENSE file for details.

## 🙏 Credits

Built with love using:
- Flask
- React
- React Native
- Discord.py
- Spotipy
- yt-dlp

## 📞 Support

For detailed setup instructions, API documentation, and troubleshooting:
- Read [DEPLOYMENT.md](./DEPLOYMENT.md)
- Check GitHub issues
- Review error logs

---

Made with ❤️ for music lovers everywhere 🎵
