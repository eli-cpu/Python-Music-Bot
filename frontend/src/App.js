import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import Login from './components/Login';
import Player from './components/Player';
import Search from './components/Search';
import Playlists from './components/Playlists';

// Set up axios defaults
axios.defaults.withCredentials = true;

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await axios.get('/api/auth/status');
      setAuthenticated(response.data.authenticated);
    } catch (error) {
      console.error('Error checking auth status:', error);
      setAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post('/api/auth/logout');
      setAuthenticated(false);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        {authenticated && (
          <nav className="navbar">
            <div className="nav-brand">
              <h1>🎵 Spotify Wrapper</h1>
            </div>
            <div className="nav-links">
              <a href="/">Player</a>
              <a href="/search">Search</a>
              <a href="/playlists">Playlists</a>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          </nav>
        )}

        <Routes>
          <Route 
            path="/login" 
            element={
              authenticated ? <Navigate to="/" /> : <Login setAuthenticated={setAuthenticated} />
            } 
          />
          <Route 
            path="/callback" 
            element={<Login setAuthenticated={setAuthenticated} />} 
          />
          <Route 
            path="/" 
            element={
              authenticated ? <Player /> : <Navigate to="/login" />
            } 
          />
          <Route 
            path="/search" 
            element={
              authenticated ? <Search /> : <Navigate to="/login" />
            } 
          />
          <Route 
            path="/playlists" 
            element={
              authenticated ? <Playlists /> : <Navigate to="/login" />
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
