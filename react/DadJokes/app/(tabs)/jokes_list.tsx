// app/(tabs)/jokes_list.tsx
// Sion Zhan (sszhan24@bu.edu), 11/12/26
// Displays a scrollable list of all jokes fetched from the REST API

import React, { useState, useCallback } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useFocusEffect } from 'expo-router';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/dadjokes';

export default function JokeListScreen() {
  const [jokes, setJokes] = useState<any[]>([]);

  const fetchJokes = () => {
    fetch(`${API_BASE}/api/jokes`)
      .then(res => res.json())
      .then(data => setJokes(data.results)) // DRF paginates
      .catch(err => console.error(err));
  };

  // useFocusEffect runs every time the tab is opened
  useFocusEffect(
    useCallback(() => {
      fetchJokes();
    }, [])
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={jokes}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.jokeText}>{item.text}</Text>
            <Text style={styles.contributorText}>added by {item.contributor}</Text>
          </View>
        )}
      />
    </View>
  );
}