// login.tsx
// Sion Zhan (sszhan24@bu.edu), 11/19/26
// RN login screen for MiniInsta app. Authenticates
// users against Django REST API and stores tokens locally

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { styles } from '../assets/my_styles';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { router } from 'expo-router';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/mini_insta';

export default function LoginScreen() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async () => {
        try {
            const response = await fetch(`${API_BASE}/api/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                await AsyncStorage.setItem('userToken', data.token);
                await AsyncStorage.setItem('profileId', data.profile_id.toString());

                // Navigate to the main tabs feed after successful login
                router.replace('/(tabs)/feed');
            } else {
                Alert.alert('Login Failed', data.non_field_errors?.[0] || 'Invalid credentials');
            }
        } catch (error) {
            console.error(error);
            Alert.alert('Error', 'Something went wrong connecting to the server.');
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>MiniInsta Login</Text>
            <TextInput
                style={styles.input}
                placeholder="Username"
                value={username}
                onChangeText={setUsername}
                autoCapitalize="none"
            />
            <TextInput
                style={styles.input}
                placeholder="Password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />
            <TouchableOpacity style={styles.button} onPress={handleLogin}>
                <Text style={styles.buttonText}>Log In</Text>
            </TouchableOpacity>
        </View>
    );
}