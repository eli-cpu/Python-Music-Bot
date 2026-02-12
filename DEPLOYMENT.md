# Spotify Wrapper - Comprehensive Documentation

## Overview

This project is a full-stack Spotify wrapper application with YouTube fallback and ad-blocking capabilities. It consists of:

1. **Backend API** - Flask-based REST API for Spotify integration and YouTube fallback
2. **Web Frontend** - React-based web application with Spotify OAuth login
3. **Discord Bot** - Existing Discord music bot (independent from web frontend)
4. **Mobile App** - React Native mobile application
5. **Vercel Deployment** - Configuration for deploying on Vercel

## Features

✅ Spotify API integration with OAuth authentication
✅ YouTube fallback when tracks are not available on Spotify
✅ Ad-blocking for YouTube streams using yt-dlp with SponsorBlock
✅ Web frontend with login capability
✅ Discord bot without login requirement (separate instance)
✅ React Native mobile app
✅ Vercel deployment ready

## Project Structure

```
Python-Music-Bot/
├── backend/                    # Flask backend API
│   ├── app.py                 # Main Flask application
│   └── requirements.txt       # Backend dependencies
├── frontend/                   # React web application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Login.js
│   │   │   ├── Player.js
│   │   │   ├── Search.js
│   │   │   └── Playlists.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   └── package.json
├── mobile/                     # React Native app
│   ├── src/
│   │   ├── screens/           # App screens
│   │   │   ├── LoginScreen.js
│   │   │   ├── HomeScreen.js
│   │   │   ├── SearchScreen.js
│   │   │   └── PlayerScreen.js
│   │   └── services/
│   │       └── ApiService.js  # API integration
│   ├── App.js
│   └── package.json
├── bot.py                      # Discord bot (existing)
├── commands/                   # Discord bot commands
├── utils/                      # Bot utilities
├── vercel.json                # Vercel deployment config
└── README.md

```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Spotify Developer Account
- Discord Bot Token (for bot functionality)

### Environment Variables

Create a `.env` file in the root directory:

```env
# Discord Bot (existing)
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CLIENT_ID=your_discord_client_id

# Spotify API
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/callback

# Flask Backend
FLASK_SECRET_KEY=your_random_secret_key
PORT=5000
```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend:
   ```bash
   python app.py
   ```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will start on `http://localhost:3000`

### Discord Bot Setup

The Discord bot runs independently from the web frontend.

1. Install dependencies (from root):
   ```bash
   pip install -r requirements.txt
   ```

2. Run the bot:
   ```bash
   python bot.py
   ```

### Mobile App Setup

1. Navigate to the mobile directory:
   ```bash
   cd mobile
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run on Android:
   ```bash
   npm run android
   ```

4. Run on iOS:
   ```bash
   npm run ios
   ```

## Backend API Endpoints

### Authentication Endpoints

- `GET /api/auth/login` - Initiate Spotify OAuth flow
- `POST /api/auth/callback` - Handle OAuth callback
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/status` - Check authentication status

### Music Endpoints

- `GET /api/search?q={query}` - Search for tracks
- `GET /api/track/{track_id}` - Get track information
- `POST /api/stream` - Get stream URL (with YouTube fallback)
  - Body: `{ "track_id": "spotify_track_id" }` or `{ "query": "search query" }`

### User Endpoints (Require Authentication)

- `GET /api/user/playlists` - Get user's playlists
- `GET /api/playlist/{playlist_id}` - Get playlist tracks
- `GET /api/user/current-track` - Get currently playing track

### Health Check

- `GET /api/health` - Health check endpoint

## Features Details

### Ad-Blocking

The backend uses `yt-dlp` with SponsorBlock integration to automatically skip:
- Sponsor segments
- Intro segments
- Outro segments
- Self-promotion segments

### YouTube Fallback

When a track is not available on Spotify or if Spotify lookup fails, the system automatically:
1. Searches YouTube for the track
2. Extracts the best audio stream
3. Provides the stream URL with ad-blocking enabled

### Authentication Flow

**Web Frontend:**
1. User clicks "Login with Spotify"
2. Redirected to Spotify OAuth page
3. After authorization, redirected back with code
4. Backend exchanges code for access token
5. Token stored in session
6. User can access protected features

**Discord Bot:**
- No authentication required
- Uses Spotify client credentials for basic track lookups
- Falls back to YouTube for streaming

## Deployment on Vercel

### Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Create a Vercel account at https://vercel.com

### Deployment Steps

1. Login to Vercel:
   ```bash
   vercel login
   ```

2. Deploy from project root:
   ```bash
   vercel
   ```

3. Set environment variables in Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add all required environment variables from `.env`

4. For production deployment:
   ```bash
   vercel --prod
   ```

### Environment Variables in Vercel

Add these as environment variables in your Vercel project:

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI` (update to your Vercel domain)
- `FLASK_SECRET_KEY`
- `DISCORD_TOKEN` (optional, if deploying bot)
- `DISCORD_CLIENT_ID` (optional, if deploying bot)

### Note on Discord Bot Deployment

The Discord bot requires a persistent connection and cannot be deployed as a serverless function on Vercel. Consider these alternatives:

1. **Deploy bot separately** on a service like:
   - Heroku
   - Railway
   - DigitalOcean
   - AWS EC2

2. **Keep bot running locally** or on a dedicated server

3. The web frontend and API can be deployed on Vercel while the bot runs elsewhere

## Discord Bot Features

The Discord bot includes these commands (see main README.md for details):

- `/play` - Play music from Spotify URL or YouTube
- `/skip` - Skip current song
- `/stop` - Stop playback
- `/pause` - Pause current song
- `/resume` - Resume playback
- `/queue` - Show queue
- `/control` - Interactive control panel (duplicate icon fixed)
- And more...

### Fixed Issue: Duplicate Icons

The GitHub button in the control panel previously had duplicate icons (both in label and emoji parameter). This has been fixed by removing the emoji from the label text.

**Before:**
```python
github_button = ui.Button(
    label="🔗 GitHub",  # Icon in label
    emoji="🔗",         # Duplicate icon
    ...
)
```

**After:**
```python
github_button = ui.Button(
    label="GitHub",     # No icon in label
    emoji="🔗",         # Single icon via emoji parameter
    ...
)
```

## Architecture

### Separation of Concerns

1. **Backend API** - Handles all Spotify/YouTube logic, authentication
2. **Web Frontend** - User-facing web application with login
3. **Discord Bot** - Separate instance for Discord users (no login needed)
4. **Mobile App** - Native mobile experience

### No Interaction Between Frontend and Bot

The web frontend and Discord bot are completely separate:
- They don't share state
- They don't communicate with each other
- They can run independently
- Each maintains its own queue and playback

## Development Tips

### Running All Services Locally

1. **Terminal 1** - Backend:
   ```bash
   cd backend && python app.py
   ```

2. **Terminal 2** - Frontend:
   ```bash
   cd frontend && npm start
   ```

3. **Terminal 3** - Discord Bot:
   ```bash
   python bot.py
   ```

### Testing the API

Use curl or Postman to test endpoints:

```bash
# Health check
curl http://localhost:5000/api/health

# Search tracks
curl http://localhost:5000/api/search?q=never+gonna+give+you+up

# Get stream (with fallback)
curl -X POST http://localhost:5000/api/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "rick astley never gonna give you up"}'
```

## Troubleshooting

### Backend Issues

- **Import errors**: Ensure all dependencies are installed
- **Spotify API errors**: Check client ID and secret
- **YouTube download fails**: Update yt-dlp: `pip install --upgrade yt-dlp`

### Frontend Issues

- **CORS errors**: Ensure backend is running and proxy is configured
- **Login fails**: Check Spotify redirect URI matches your setup
- **Build fails**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### Discord Bot Issues

- **Bot not responding**: Check Discord token in `.env`
- **Voice connection fails**: Ensure PyNaCl is installed
- **Playback issues**: Check FFmpeg is installed

## Security Considerations

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use environment variables** for all secrets in production
3. **Rotate tokens regularly** - Especially Spotify access tokens
4. **HTTPS in production** - Always use HTTPS for the web frontend
5. **Rate limiting** - Consider adding rate limiting to API endpoints

## Future Enhancements

Potential features to add:

- [ ] Queue management in web frontend
- [ ] Playlist creation and editing
- [ ] Social features (share playlists)
- [ ] Lyrics integration
- [ ] Audio visualization
- [ ] Podcast support
- [ ] Download for offline playback
- [ ] Cross-device sync

## License

See LICENSE file for details.

## Support

For issues and questions:
1. Check existing documentation
2. Review error messages carefully
3. Check GitHub issues
4. Contact maintainers

## Credits

Built with:
- Flask (Backend)
- React (Web Frontend)
- React Native (Mobile App)
- Discord.py (Bot)
- Spotipy (Spotify API)
- yt-dlp (YouTube integration)
