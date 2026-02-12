import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Playlists() {
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPlaylists();
  }, []);

  const fetchPlaylists = async () => {
    try {
      const response = await axios.get('/api/user/playlists');
      setPlaylists(response.data.playlists);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching playlists:', error);
      setLoading(false);
    }
  };

  const fetchPlaylistDetails = async (playlistId) => {
    try {
      const response = await axios.get(`/api/playlist/${playlistId}`);
      setSelectedPlaylist(response.data);
    } catch (error) {
      console.error('Error fetching playlist details:', error);
      alert('Failed to load playlist details.');
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading playlists...</div>
      </div>
    );
  }

  if (selectedPlaylist) {
    return (
      <div className="container">
        <div className="card">
          <button 
            onClick={() => setSelectedPlaylist(null)}
            className="btn"
            style={{ marginBottom: '2rem' }}
          >
            ← Back to Playlists
          </button>

          <div style={{ display: 'flex', gap: '2rem', marginBottom: '2rem' }}>
            {selectedPlaylist.image && (
              <img 
                src={selectedPlaylist.image} 
                alt={selectedPlaylist.name}
                style={{ width: '200px', height: '200px', borderRadius: '8px' }}
              />
            )}
            <div>
              <h2>{selectedPlaylist.name}</h2>
              {selectedPlaylist.description && (
                <p style={{ color: '#b3b3b3', marginTop: '0.5rem' }}>
                  {selectedPlaylist.description}
                </p>
              )}
              <p style={{ color: '#b3b3b3', marginTop: '1rem' }}>
                {selectedPlaylist.tracks.length} tracks
              </p>
            </div>
          </div>

          <div className="track-list">
            {selectedPlaylist.tracks.map((track, index) => (
              <div key={track.id} className="track-item">
                <span style={{ color: '#b3b3b3', marginRight: '1rem' }}>
                  {index + 1}
                </span>
                {track.image && (
                  <img 
                    src={track.image} 
                    alt={track.name}
                    className="track-image"
                  />
                )}
                <div className="track-info">
                  <div className="track-name">{track.name}</div>
                  <div className="track-artist">{track.artists.join(', ')}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card">
        <h2 style={{ marginBottom: '2rem' }}>Your Playlists</h2>
        
        {playlists.length > 0 ? (
          <div className="playlist-grid">
            {playlists.map((playlist) => (
              <div 
                key={playlist.id} 
                className="playlist-card"
                onClick={() => fetchPlaylistDetails(playlist.id)}
              >
                {playlist.image && (
                  <img 
                    src={playlist.image} 
                    alt={playlist.name}
                    className="playlist-image"
                  />
                )}
                <div className="playlist-name">{playlist.name}</div>
                <div className="playlist-tracks">{playlist.tracks_total} tracks</div>
              </div>
            ))}
          </div>
        ) : (
          <p style={{ color: '#b3b3b3', textAlign: 'center', padding: '2rem' }}>
            No playlists found
          </p>
        )}
      </div>
    </div>
  );
}

export default Playlists;
