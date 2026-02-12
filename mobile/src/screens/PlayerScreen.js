import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import ApiService from '../services/ApiService';

function PlayerScreen({ route, navigation }) {
  const [track, setTrack] = useState(route.params?.track || null);
  const [loading, setLoading] = useState(false);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    if (!track) {
      loadCurrentTrack();
    }
  }, []);

  const loadCurrentTrack = async () => {
    setLoading(true);
    try {
      const currentTrack = await ApiService.getCurrentTrack();
      setTrack(currentTrack);
    } catch (error) {
      console.error('Error loading current track:', error);
    } finally {
      setLoading(false);
    }
  };

  const playTrack = async () => {
    if (!track) return;

    setLoading(true);
    try {
      const streamData = await ApiService.getStream(track.id);
      
      // TODO: Integrate react-native-track-player for actual audio playback
      // Currently displays URL for development/testing purposes
      // See: https://github.com/doublesymmetry/react-native-track-player
      console.log('Stream URL:', streamData.url);
      setPlaying(true);
      alert('Audio player integration in progress. Stream URL logged to console.');
    } catch (error) {
      console.error('Error playing track:', error);
      alert('Failed to play track');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !track) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#1DB954" />
      </View>
    );
  }

  if (!track) {
    return (
      <View style={styles.container}>
        <Text style={styles.emptyText}>No track playing</Text>
        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate('Search')}
        >
          <Text style={styles.buttonText}>Search Music</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Image
        source={{ uri: track.image }}
        style={styles.albumArt}
      />
      
      <Text style={styles.trackName}>{track.name}</Text>
      <Text style={styles.artistName}>
        {Array.isArray(track.artists) ? track.artists.join(', ') : track.artists}
      </Text>
      <Text style={styles.albumName}>{track.album}</Text>

      <View style={styles.controls}>
        <TouchableOpacity
          style={styles.playButton}
          onPress={playTrack}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.playButtonText}>
              {playing ? '⏸️ Pause' : '▶️ Play'}
            </Text>
          )}
        </TouchableOpacity>
      </View>

      <View style={styles.infoBox}>
        <Text style={styles.infoText}>
          🎵 Playing via YouTube with ad-blocking enabled
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  albumArt: {
    width: 300,
    height: 300,
    borderRadius: 8,
    marginBottom: 30,
  },
  trackName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 10,
  },
  artistName: {
    fontSize: 18,
    color: '#b3b3b3',
    textAlign: 'center',
    marginBottom: 5,
  },
  albumName: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 20,
  },
  playButton: {
    backgroundColor: '#1DB954',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 30,
    minWidth: 150,
    alignItems: 'center',
  },
  playButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  button: {
    backgroundColor: '#1DB954',
    paddingHorizontal: 30,
    paddingVertical: 12,
    borderRadius: 25,
    marginTop: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  emptyText: {
    color: '#b3b3b3',
    fontSize: 18,
    marginBottom: 20,
  },
  infoBox: {
    backgroundColor: '#181818',
    padding: 15,
    borderRadius: 8,
    marginTop: 20,
  },
  infoText: {
    color: '#1DB954',
    textAlign: 'center',
  },
});

export default PlayerScreen;
