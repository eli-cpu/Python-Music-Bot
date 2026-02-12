import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  FlatList,
  Image,
  ActivityIndicator,
} from 'react-native';
import ApiService from '../services/ApiService';

function SearchScreen({ navigation }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const data = await ApiService.searchTracks(query);
      setResults(data.tracks);
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderTrack = ({ item }) => (
    <TouchableOpacity
      style={styles.trackItem}
      onPress={() => navigation.navigate('Player', { track: item })}
    >
      {item.image && (
        <Image source={{ uri: item.image }} style={styles.trackImage} />
      )}
      <View style={styles.trackInfo}>
        <Text style={styles.trackName} numberOfLines={1}>
          {item.name}
        </Text>
        <Text style={styles.trackArtist} numberOfLines={1}>
          {item.artists.join(', ')}
        </Text>
        <Text style={styles.trackAlbum} numberOfLines={1}>
          {item.album}
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search for songs, artists, or albums..."
          placeholderTextColor="#666"
          value={query}
          onChangeText={setQuery}
          onSubmitEditing={handleSearch}
        />
        <TouchableOpacity
          style={styles.searchButton}
          onPress={handleSearch}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.searchButtonText}>Search</Text>
          )}
        </TouchableOpacity>
      </View>

      <FlatList
        data={results}
        renderItem={renderTrack}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.resultsList}
        ListEmptyComponent={
          <Text style={styles.emptyText}>
            {loading ? 'Searching...' : 'Search for music to get started'}
          </Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  searchContainer: {
    flexDirection: 'row',
    padding: 15,
    gap: 10,
  },
  searchInput: {
    flex: 1,
    backgroundColor: '#282828',
    color: '#fff',
    padding: 12,
    borderRadius: 25,
    fontSize: 16,
  },
  searchButton: {
    backgroundColor: '#1DB954',
    paddingHorizontal: 25,
    paddingVertical: 12,
    borderRadius: 25,
    justifyContent: 'center',
  },
  searchButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  resultsList: {
    padding: 15,
  },
  trackItem: {
    flexDirection: 'row',
    backgroundColor: '#181818',
    borderRadius: 8,
    padding: 10,
    marginBottom: 10,
  },
  trackImage: {
    width: 60,
    height: 60,
    borderRadius: 4,
  },
  trackInfo: {
    flex: 1,
    marginLeft: 10,
    justifyContent: 'center',
  },
  trackName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 3,
  },
  trackArtist: {
    color: '#b3b3b3',
    fontSize: 14,
    marginBottom: 2,
  },
  trackAlbum: {
    color: '#666',
    fontSize: 12,
  },
  emptyText: {
    color: '#b3b3b3',
    textAlign: 'center',
    marginTop: 50,
    fontSize: 16,
  },
});

export default SearchScreen;
