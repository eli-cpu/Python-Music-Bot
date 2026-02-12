import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';

function HomeScreen({ navigation }) {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.welcomeText}>Welcome to Spotify Wrapper</Text>
        
        <TouchableOpacity
          style={styles.card}
          onPress={() => navigation.navigate('Search')}
        >
          <Text style={styles.cardIcon}>🔍</Text>
          <Text style={styles.cardTitle}>Search Music</Text>
          <Text style={styles.cardDescription}>
            Search for songs on Spotify with YouTube fallback
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.card}
          onPress={() => navigation.navigate('Player')}
        >
          <Text style={styles.cardIcon}>🎵</Text>
          <Text style={styles.cardTitle}>Now Playing</Text>
          <Text style={styles.cardDescription}>
            View and control currently playing track
          </Text>
        </TouchableOpacity>

        <View style={styles.infoCard}>
          <Text style={styles.infoTitle}>Features:</Text>
          <Text style={styles.infoText}>✅ Spotify integration</Text>
          <Text style={styles.infoText}>✅ YouTube fallback for unavailable tracks</Text>
          <Text style={styles.infoText}>✅ Ad-blocking enabled</Text>
          <Text style={styles.infoText}>✅ High-quality audio streaming</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  content: {
    padding: 20,
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 30,
  },
  card: {
    backgroundColor: '#181818',
    borderRadius: 10,
    padding: 20,
    marginBottom: 15,
  },
  cardIcon: {
    fontSize: 40,
    marginBottom: 10,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  cardDescription: {
    fontSize: 14,
    color: '#b3b3b3',
  },
  infoCard: {
    backgroundColor: '#1DB954',
    borderRadius: 10,
    padding: 20,
    marginTop: 20,
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  infoText: {
    fontSize: 14,
    color: '#fff',
    marginBottom: 5,
  },
});

export default HomeScreen;
