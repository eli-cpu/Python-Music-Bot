import React, { useState, useRef } from 'react';
import axios from 'axios';

function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const audioRef = useRef(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.get(`/api/search?q=${encodeURIComponent(query)}`);
      setResults(response.data.tracks);
    } catch (error) {
      console.error('Error searching:', error);
      alert('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const playTrack = async (trackId, trackName) => {
    try {
      const response = await axios.post('/api/stream', { track_id: trackId });
      if (audioRef.current && response.data.url) {
        audioRef.current.src = response.data.url;
        audioRef.current.play();
        alert(`Now playing: ${trackName}`);
      }
    } catch (error) {
      console.error('Error playing track:', error);
      alert('Failed to play track. Trying YouTube fallback...');
      
      // Try direct YouTube search as fallback
      try {
        const fallbackResponse = await axios.post('/api/stream', { 
          query: trackName 
        });
        if (audioRef.current && fallbackResponse.data.url) {
          audioRef.current.src = fallbackResponse.data.url;
          audioRef.current.play();
        }
      } catch (fallbackError) {
        console.error('YouTube fallback failed:', fallbackError);
        alert('Could not play this track.');
      }
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2 style={{ marginBottom: '2rem' }}>Search Music</h2>
        
        <form onSubmit={handleSearch}>
          <input
            type="text"
            className="search-box"
            placeholder="Search for songs, artists, or albums..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {results.length > 0 && (
          <div className="track-list" style={{ marginTop: '2rem' }}>
            {results.map((track) => (
              <div 
                key={track.id} 
                className="track-item"
              >
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
                  <div className="track-artist">{track.album}</div>
                </div>
                <button 
                  className="btn" 
                  style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}
                  onClick={() => playTrack(track.id, `${track.name} ${track.artists.join(' ')}`)}
                >
                  Play
                </button>
              </div>
            ))}
          </div>
        )}

        <audio ref={audioRef} controls style={{ width: '100%', marginTop: '2rem' }} />
      </div>
    </div>
  );
}

export default Search;
