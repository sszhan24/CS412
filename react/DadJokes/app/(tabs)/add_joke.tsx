// app/(tabs)/add_joke.tsx
// Sion Zhan (sszhan24@bu.edu), 11/12/26
// Provides a form to create a new joke an POST it to the REST API

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { styles } from '../../assets/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/sszhan24/dadjokes/';

export default function AddJokeScreen() {
    const [text, setText] = useState('');
    const [contributor, setContributor] = useState('');

    const submitJoke = () => {
        if (!text || !contributor) {
            Alert.alert("Error", "Please fill out all fields.");
            return;
        }

        // POST request to the API
        fetch(`${API_BASE}/api/jokes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                contributor: contributor,
            }),
        })
            .then(res => {
                console.log("Status Code:", res.status); // Should be 201 created
                if (res.status == 201) {
                    Alert.alert("Success", "Joke added!");
                    setText('');
                    setContributor('');
                }
            })
            .catch(err => console.error(err));
    };

    return (
        <View style={styles.container}>
            <View style={styles.card}>
                <Text style={{ fontSize: 24, marginBottom: 15 }}>Add a Joke</Text>

                <Text style={{ fontSize: 18, color: '#00008b' }}>What's your Joke?</Text>
                <TextInput
                    style={[styles.input, { height: 100 }]}
                    multiline
                    placeholder="Joke"
                    value={text}
                    onChangeText={setText}
                />
                <Text style={{ fontSize: 18, color: '#00008b' }}>Contributed by</Text>
                <TextInput
                    style={styles.input}
                    placeholder="Your Name"
                    value={contributor}
                    onChangeText={setContributor}
                />

                <TouchableOpacity style={styles.button} onPress={submitJoke}>
                    <Text style={styles.buttonText}>Add Joke</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}