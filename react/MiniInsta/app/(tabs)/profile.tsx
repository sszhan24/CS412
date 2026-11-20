// profile.tsx
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Displays the profile details and posts for a specific user

import React, { useState, useCallback } from 'react';
import { useFocusEffect, router } from 'expo-router';
import { View, Text, Image, ScrollView, TouchableOpacity, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/mini_insta';
//const PROFILE_ID = 5;

/**
 * the profile screen component
 * fetches and displays the user's data and their posts
 */

export default function ProfileScreen() {
    const [profile, setProfile] = useState<any>(null);
    const [posts, setPosts] = useState<any[]>([]);

    /*

    useEffect(() => {
        fetch(`${API_BASE}/api/profiles/${PROFILE_ID}/`)
            .then(res => res.json())
            .then(data => setProfile(data));
        
        fetch(`${API_BASE}/api/profiles/${PROFILE_ID}/posts/`)
            .then(res => res.json())
            .then(data => setPosts(data.results))
            .catch(err => console.error(err));
    }, []);
    */

    const fetchData = async () => {
        try {
            const token = await AsyncStorage.getItem('userToken');
            const profileId = await AsyncStorage.getItem('profileId');

            if (!token || !profileId) {
                console.log('No authentication token found');
                return;
            }

            // Fetch profile info with auth header
            const profileRes = await fetch(`${API_BASE}/api/profiles/${profileId}/`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
            });
            const profileData = await profileRes.json();
            if (profileRes.ok) {
                setProfile(profileData);
            }

            // fetch profile posts with auth header
            const postsRes = await fetch(`${API_BASE}/api/profiles/${profileId}/posts/`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':   `Token ${token}`,
                },
            });
            const postsData = await postsRes.json();
            if (postsRes.ok) {
                setPosts(postsData.results || postsData);
            }
        } catch (err) {
            console.error('Error fetching profile data:', err);
        }
    };

    const handleLogout = async () => {
        try {
            await AsyncStorage.removeItem('userToken');
            await AsyncStorage.removeItem('profileId');
            router.replace('/login');
        } catch (error) {
            console.error('Failed to log out:', error);
            Alert.alert('Error', 'Could not log out properly');
        }
    };

    // Automatically fetch fresh data every time this screen comes into focus
    useFocusEffect(
        useCallback(() => {
            fetchData();
        }, [])
    );

    if (!profile) return <Text style={{ padding: 20 }}>Loading...</Text>;

    return (
        <ScrollView style={styles.container} contentContainerStyle= {{ paddingBottom: 40 }}>
            <View style={styles.card}>
                {profile.profile_image_url && (
                    <Image source={{ uri: profile.profile_image_url }} style={{ width: 100, height: 100, borderRadius: 50, alignSelf: 'center', marginBottom: 10 }} />
                )}
                <Text style={{ fontSize: 22, fontWeight: 'bold', textAlign: 'center' }}>{profile.username}</Text>
                <Text style={{ textAlign: 'center', color: 'gray', marginBottom: 10 }}>{profile.display_name}</Text>
                <Text>{profile.bio_text}</Text>

                {/* logout button */}
                <TouchableOpacity style={styles.button} onPress={handleLogout}>
                    <Text style={styles.buttonText}>Log Out</Text>
                </TouchableOpacity>
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