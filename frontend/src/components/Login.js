import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Login({ setAuthenticated }) {
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check if we're on the callback page
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    
    if (code) {
      handleCallback(code);
    }
  }, []);

  const handleCallback = async (code) => {
    setLoading(true);
    try {
      await axios.post('/api/auth/callback', { code });
      setAuthenticated(true);
      window.location.href = '/';
    } catch (error) {
      console.error('Error during callback:', error);
      alert('Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/auth/login');
      window.location.href = response.data.auth_url;
    } catch (error) {
      console.error('Error initiating login:', error);
      alert('Failed to initiate login. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card" style={{ textAlign: 'center', maxWidth: '500px', margin: '5rem auto' }}>
        <h1 style={{ marginBottom: '2rem', color: '#1DB954' }}>🎵 Welcome to Spotify Wrapper</h1>
        <p style={{ marginBottom: '2rem', color: '#b3b3b3' }}>
          Login with your Spotify account to start streaming music with YouTube fallback and ad blocking!
        </p>
        <button 
          onClick={handleLogin} 
          className="btn" 
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Login with Spotify'}
        </button>
      </div>
    </div>
  );
}

export default Login;
