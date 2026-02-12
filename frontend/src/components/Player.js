import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function Player() {
  const [currentTrack, setCurrentTrack] = useState(null);
  const [loading, setLoading] = useState(true);
  const audioRef = useRef(null);

  useEffect(() => {
    fetchCurrentTrack();
    const interval = setInterval(fetchCurrentTrack, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchCurrentTrack = async () => {
    try {
      const response = await axios.get('/api/user/current-track');
      setCurrentTrack(response.data);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      if (error.response?.status !== 404) {
        console.error('Error fetching current track:', error);
      }
    }
  };

  const playTrack = async (trackId) => {
    try {
      const response = await axios.post('/api/stream', { track_id: trackId });
      if (audioRef.current && response.data.url) {
        audioRef.current.src = response.data.url;
        audioRef.current.play();
      }
    } catch (error) {
      console.error('Error playing track:', error);
      alert('Failed to play track. It might not be available.');
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading player...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card player-container">
        <h2 style={{ marginBottom: '2rem' }}>Now Playing</h2>
        
        {currentTrack ? (
          <div className="current-track">
            {currentTrack.image && (
              <img 
                src={currentTrack.image} 
                alt={currentTrack.name}
                className="current-track-image"
              />
            )}
            <div style={{ textAlign: 'center' }}>
              <h3>{currentTrack.name}</h3>
              <p style={{ color: '#b3b3b3', marginTop: '0.5rem' }}>
                {currentTrack.artists.join(', ')}
              </p>
              <p style={{ color: '#b3b3b3', marginTop: '0.5rem' }}>
                Album: {currentTrack.album}
              </p>
              {currentTrack.is_playing ? (
                <p style={{ color: '#1DB954', marginTop: '1rem', fontSize: '1.2rem' }}>
                  ▶️ Playing
                </p>
              ) : (
                <p style={{ color: '#b3b3b3', marginTop: '1rem', fontSize: '1.2rem' }}>
                  ⏸️ Paused
                </p>
              )}
              <button 
                onClick={() => playTrack(currentTrack.id)}
                className="btn"
                style={{ marginTop: '1rem' }}
              >
                Play via YouTube (Ad-Free)
              </button>
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: '#b3b3b3', fontSize: '1.2rem' }}>
              No track currently playing
            </p>
            <p style={{ color: '#b3b3b3', marginTop: '1rem' }}>
              Start playing music on Spotify or use the search page
            </p>
          </div>
        )}

        <audio ref={audioRef} controls style={{ width: '100%', marginTop: '2rem' }} />
      </div>
    </div>
  );
}

export default Player;
