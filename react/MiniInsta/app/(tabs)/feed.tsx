// feed.tsx
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Displays the post feed for a specific profile

import React, { useState, useCallback } from 'react';
import { View, Text, Image, FlatList } from 'react-native';
import { useFocusEffect } from 'expo-router';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/mini_insta';
const PROFILE_ID = 5;

/**
 * the feed screen component
 * fetches and displays posts from profiles the hardcoded user follows
 */
export default function FeedScreen() {
    const [feed, setFeed] = useState<any[]>([]);
    
    const fetchFeed = () => {
      fetch(`${API_BASE}/api/profiles/${PROFILE_ID}/feed/`)
        .then(res => res.json())
        .then(data => setFeed(data))
        .catch(err => console.error(err));
    };

    useFocusEffect(useCallback(() => { fetchFeed(); }, []));
    
    return (
      <View style={styles.container}>
        <FlatList
          data={feed}
          keyExtractor={item => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={styles.username}>@{item.author_username}</Text>
              {item.photos && item.photo.length > 0 && item.photos[0].image_url ? (
                <Image source={{ uri: item.photos[0].image_url }} style={styles.image} />
              ) : null}
              <Text style={styles.caption}>{item.caption}</Text>
            </View>
          )}
          ListEmptyComponent={<Text>No posts in feed yet</Text>}
          />
      </View>
    );
}