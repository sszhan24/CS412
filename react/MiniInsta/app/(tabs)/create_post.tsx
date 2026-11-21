// create_post.tsx
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Provides a form to create a new post and POST it to the API

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { router } from 'expo-router';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/mini_insta';
//const PROFILE_ID = 5;

/**
 * the create post screen component
 * allows the uesr to type a caption and submit a POST request
 */

export default function CreatePostScreen() {
  const [caption, setCaption] = useState('');

  /**
   * submits the new post to the API
   */
  const submitPost = async () => {
    if (!caption) {
      Alert.alert("Error", "Please enter a caption");
      return;
    }

    try {
      const token = await AsyncStorage.getItem('userToken');
      const profileId = await AsyncStorage.getItem('profileId');

      if (!token || !profileId) {
        Alert.alert("Error", "You must be logged in to create a post");
        return;
      }

      const response = await fetch(`${API_BASE}/api/posts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', 
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
          profile: parseInt(profileId, 10),
          caption: caption
        })
      });
      
      console.log("Status:", response.status);

      if (response.status === 201) {
        Alert.alert("Success", "Post created!");
        setCaption('');
        // automatically navigate back to feed after posting
        router.replace('/(tabs)/feed');
      } else {
        const data = await response.json();
        Alert.alert("Error", "Failed to create post.");
        console.error(data);
      }
    } catch (err) {
      console.error(err);
      Alert.alert("Error", "Something went wrong connecting to the server");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={{ fontSize: 22, fontWeight: 'bold', marginBottom: 15 }}>New Post</Text>

      <TextInput
        style={[styles.input, { height: 100 }]}
        multiline
        placeholder="What's up?"
        value={caption}
        onChangeText={setCaption}
        returnKeyType="done"
        blurOnSubmit={true}
      />
      <TouchableOpacity style={styles.button} onPress={submitPost}>
        <Text style={styles.buttonText}>Post</Text>
      </TouchableOpacity>
    </View>
  );
}