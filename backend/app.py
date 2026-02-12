"""
Flask backend for Spotify wrapper with YouTube fallback and ad blocking
"""
import os
import re
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests
from functools import wraps
import yt_dlp

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
CORS(app, supports_credentials=True)

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:3000/callback')

# Spotify OAuth setup for user authentication
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope='user-read-playback-state user-modify-playback-state user-read-currently-playing streaming user-library-read user-library-modify playlist-read-private playlist-read-collaborative'
)

# Spotify client credentials for basic access (without user login)
client_credentials = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
sp_client = spotipy.Spotify(client_credentials_manager=client_credentials)

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_info = session.get('token_info')
        if not token_info:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Check if token is expired and refresh if needed
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
        
        return f(*args, **kwargs)
    return decorated_function

def get_youtube_stream(query):
    """
    Get YouTube stream URL for a search query
    Blocks ads by using yt-dlp with specific options
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'default_search': 'ytsearch1',
        # Ad blocking configurations
        'sponsorblock_remove': ['sponsor', 'intro', 'outro', 'selfpromo'],
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['hls', 'dash']
            }
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if query.startswith('http'):
                # Direct URL
                info = ydl.extract_info(query, download=False)
            else:
                # Search query
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
            
            # Get the best audio stream URL
            if 'url' in info:
                stream_url = info['url']
            elif 'formats' in info:
                # Find best audio format
                audio_formats = [f for f in info['formats'] if f.get('acodec') != 'none']
                if audio_formats:
                    best_audio = max(audio_formats, key=lambda f: f.get('abr', 0))
                    stream_url = best_audio['url']
                else:
                    stream_url = info['formats'][-1]['url']
            else:
                return None
            
            return {
                'url': stream_url,
                'title': info.get('title'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail')
            }
    except Exception as e:
        print(f"Error getting YouTube stream: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

@app.route('/api/auth/login', methods=['GET'])
def login():
    """Initiate Spotify OAuth flow"""
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({'auth_url': auth_url})

@app.route('/api/auth/callback', methods=['POST'])
def callback():
    """Handle Spotify OAuth callback"""
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info
        return jsonify({'message': 'Authentication successful', 'token_info': token_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.pop('token_info', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    token_info = session.get('token_info')
    if token_info:
        # Check if token is expired
        if sp_oauth.is_token_expired(token_info):
            return jsonify({'authenticated': False})
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False})

@app.route('/api/track/<track_id>', methods=['GET'])
def get_track(track_id):
    """Get track information from Spotify"""
    try:
        token_info = session.get('token_info')
        if token_info:
            sp = spotipy.Spotify(auth=token_info['access_token'])
        else:
            sp = sp_client
        
        track = sp.track(track_id)
        return jsonify({
            'id': track['id'],
            'name': track['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'album': track['album']['name'],
            'duration_ms': track['duration_ms'],
            'preview_url': track['preview_url'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'spotify_url': track['external_urls']['spotify']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/search', methods=['GET'])
def search():
    """Search for tracks on Spotify"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        token_info = session.get('token_info')
        if token_info:
            sp = spotipy.Spotify(auth=token_info['access_token'])
        else:
            sp = sp_client
        
        results = sp.search(q=query, type='track', limit=20)
        tracks = []
        for item in results['tracks']['items']:
            tracks.append({
                'id': item['id'],
                'name': item['name'],
                'artists': [artist['name'] for artist in item['artists']],
                'album': item['album']['name'],
                'duration_ms': item['duration_ms'],
                'preview_url': item['preview_url'],
                'image': item['album']['images'][0]['url'] if item['album']['images'] else None,
                'spotify_url': item['external_urls']['spotify']
            })
        
        return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stream', methods=['POST'])
def get_stream():
    """
    Get stream URL for a track
    First tries Spotify, then falls back to YouTube if not found
    """
    data = request.json
    track_id = data.get('track_id')
    query = data.get('query')
    
    if not track_id and not query:
        return jsonify({'error': 'Either track_id or query is required'}), 400
    
    # Try to get track info from Spotify first
    if track_id:
        try:
            token_info = session.get('token_info')
            if token_info:
                sp = spotipy.Spotify(auth=token_info['access_token'])
            else:
                sp = sp_client
            
            track = sp.track(track_id)
            query = f"{track['name']} {' '.join([artist['name'] for artist in track['artists']])}"
        except Exception as e:
            # If Spotify fails, try YouTube directly with the query
            print(f"Spotify lookup failed: {e}, falling back to YouTube")
    
    # Get YouTube stream (with ad blocking)
    if query:
        stream_info = get_youtube_stream(query)
        if stream_info:
            return jsonify(stream_info)
        else:
            return jsonify({'error': 'Could not find stream'}), 404
    
    return jsonify({'error': 'Failed to get stream'}), 500

@app.route('/api/playlist/<playlist_id>', methods=['GET'])
@require_auth
def get_playlist(playlist_id):
    """Get playlist tracks"""
    try:
        token_info = session.get('token_info')
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        playlist = sp.playlist(playlist_id)
        tracks = []
        for item in playlist['tracks']['items']:
            track = item['track']
            if track:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artists': [artist['name'] for artist in track['artists']],
                    'album': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'image': track['album']['images'][0]['url'] if track['album']['images'] else None
                })
        
        return jsonify({
            'name': playlist['name'],
            'description': playlist['description'],
            'tracks': tracks,
            'image': playlist['images'][0]['url'] if playlist['images'] else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/user/playlists', methods=['GET'])
@require_auth
def get_user_playlists():
    """Get user's playlists"""
    try:
        token_info = session.get('token_info')
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        playlists = sp.current_user_playlists(limit=50)
        result = []
        for playlist in playlists['items']:
            result.append({
                'id': playlist['id'],
                'name': playlist['name'],
                'tracks_total': playlist['tracks']['total'],
                'image': playlist['images'][0]['url'] if playlist['images'] else None,
                'public': playlist['public']
            })
        
        return jsonify({'playlists': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/current-track', methods=['GET'])
@require_auth
def get_current_track():
    """Get user's currently playing track"""
    try:
        token_info = session.get('token_info')
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        current = sp.current_playback()
        if current and current['item']:
            track = current['item']
            return jsonify({
                'id': track['id'],
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'progress_ms': current['progress_ms'],
                'is_playing': current['is_playing'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None
            })
        else:
            return jsonify({'message': 'No track currently playing'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
