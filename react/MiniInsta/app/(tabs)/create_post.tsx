// create_post.tsx
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Provides a form to create a new post and POST it to the API

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/mini_insta';
const PROFILE_ID = 5;

/**
 * the create post screen component
 * allows the uesr to type a caption and submit a POST request
 */

export default function CreatePostScreen() {
  const [caption, setCaption] = useState('');

  /**
   * submits the new post to the API
   */
  const submitPost = () => {
    if (!caption) {
      Alert.alert("Error", "Please enter a caption");
      return;
    }

    fetch(`${API_BASE}/api/posts/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile: PROFILE_ID, caption: caption })
    })
      .then(res => {
        console.log("Status:", res.status);
        if (res.status == 201) {
          Alert.alert("Success", "Post created!");
          setCaption('');
        }
      })
      .catch(err => console.error(err));
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
      />
      <TouchableOpacity style={styles.button} onPress={submitPost}>
        <Text style={styles.buttonText}>Post</Text>
      </TouchableOpacity>
    </View>
  );
}