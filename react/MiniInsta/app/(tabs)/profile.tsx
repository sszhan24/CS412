// profile.tsx
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Displays the profile details and posts for a specific user

import React, { useState, useEffect } from 'react';
import { View, Text, Image, ScrollView } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/mini_insta';
const PROFILE_ID = 5;

/**
 * the profile screen component
 * fetches and displays the user's data and their posts
 */

export default function ProfileScreen() {
    const [profile, setProfile] = useState<any>(null);
    const [posts, setPosts] = useState<any[]>([]);

    useEffect(() => {
        fetch(`${API_BASE}/api/profiles/${PROFILE_ID}/`)
            .then(res => res.json())
            .then(data => setProfile(data));
        
        fetch(`${API_BASE}/api/profiles/${PROFILE_ID}/posts/`)
            .then(res => res.json())
            .then(data => setPosts(data));
    }, []);

    if (!profile) return <Text>Loading...</Text>;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.card}>
                {profile.profile_image_url && (
                    <Image source={{ uri: profile.profile_image_url }} style={{ width: 100, height: 100, borderRadius: 50, alignSelf: 'center', marginBottom: 10 }} />
                )}
                <Text style={{ fontSize: 22, fontWeight: 'bold', textAlign: 'center' }}>{profile.username}</Text>
                <Text style={{ textAlign: 'center', color: 'gray', marginBottom: 10 }}>{profile.display_name}</Text>
                <Text>{profile.bio_text}</Text>
            </View>

            <Text style={{ fontSize: 20, fontWeight: 'bold', marginVertical: 15 }}>My Posts</Text>
            {posts.map(post => (
                <View key={post.id} style={styles.card}>
                    <Text style={styles.caption}>{post.caption}</Text>
                    {post.photos && post.photos.length > 0 && post.photos[0].image_url ? (
                        <Image source={{ uri: post.photos[0].image_url }} style={styles.image} />
                    ) : null}
                </View>
            ))}
        </ScrollView>
    );
}