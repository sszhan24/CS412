// app/(tabs)/index.tsx
// Sion Zhan (sszhan24@bu.edu), 11/12/26
// Displays a random joke and picture fetched from the REST API

import React, { useState, useEffect } from 'react';
import { View, Text, Image, TouchableOpacity, ScrollView } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/dadjokes';

export default function IndexScreen() {
  const [joke, setJoke] = useState<any>(null);
  const [picture, setPicture] = useState<any>(null);

  const fetchData = () => {
    fetch(`${API_BASE}/api/random`)
      .then(res => res.json())
      .then(data => setJoke(data))
      .catch(err => console.error(err));

    fetch(`${API_BASE}/api/random_picture`)
      .then(res => res.json())
      .then(data => setPicture(data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.card}>
        {joke ? (
          <>
            <Text style={styles.jokeText}>"{joke.text}"</Text>
            <Text style={styles.contributorText}>added by {joke.contributor}</Text>
          </>
        ) : (
          <Text>Loading joke...</Text>
        )}

        {picture && (
          <Image source={{ uri: picture.image_url }} style={styles.image} />
        )}
      </View>

      <TouchableOpacity style={styles.button} onPress={fetchData}>
        <Text style={styles.buttonText}>Tell me another!</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}