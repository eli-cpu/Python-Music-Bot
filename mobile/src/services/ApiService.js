import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      withCredentials: true,
    });
  }

  async login() {
    const response = await this.client.get('/auth/login');
    return response.data;
  }

  async handleCallback(code) {
    const response = await this.client.post('/auth/callback', { code });
    if (response.data.token_info) {
      await AsyncStorage.setItem('token_info', JSON.stringify(response.data.token_info));
    }
    return response.data;
  }

  async checkAuth() {
    const response = await this.client.get('/auth/status');
    return response.data;
  }

  async logout() {
    await this.client.post('/auth/logout');
    await AsyncStorage.removeItem('token_info');
  }

  async searchTracks(query) {
    const response = await this.client.get(`/search?q=${encodeURIComponent(query)}`);
    return response.data;
  }

  async getTrack(trackId) {
    const response = await this.client.get(`/track/${trackId}`);
    return response.data;
  }

  async getStream(trackId, query) {
    const data = {};
    if (trackId) data.track_id = trackId;
    if (query) data.query = query;
    
    const response = await this.client.post('/stream', data);
    return response.data;
  }

  async getUserPlaylists() {
    const response = await this.client.get('/user/playlists');
    return response.data;
  }

  async getPlaylist(playlistId) {
    const response = await this.client.get(`/playlist/${playlistId}`);
    return response.data;
  }

  async getCurrentTrack() {
    const response = await this.client.get('/user/current-track');
    return response.data;
  }
}

export default new ApiService();
