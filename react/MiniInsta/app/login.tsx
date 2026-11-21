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
        await AsyncStorage.multiRemove(['userToken', 'profileId']);

        try {
            const response = await fetch(`${API_BASE}/api/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username.trim(), password }),
            });

           // 1. Read raw text first and log it so you can see the exact server reply
            const rawText = await response.text();
            console.log('Login Status:', response.status);
            console.log('Server Reply:', rawText);

            // 2. Parse the text into a JSON object
            let data;
            try {
                data = JSON.parse(rawText);
            } catch (e) {
                Alert.alert('Server Error', `Status ${response.status}: Server returned HTML/text instead of JSON.`);
                return;
            }

            if (response.ok) {
                if (data.profile_id == null) {
                    Alert.alert('No Profile', 'This account has no profile yet.');
                    return;
                }
                await AsyncStorage.setItem('userToken', data.token);
                await AsyncStorage.setItem('profileId', String(data.profile_id));
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