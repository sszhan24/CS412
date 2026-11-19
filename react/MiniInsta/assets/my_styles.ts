// my_styles.ts
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Defines shared styling rules for the MiniInsta React Native app

import { StyleSheet } from 'react-native';

// Export the shared stylehseet object so it can be imported by any screen
export const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5', padding: 15 },
    card: { backgroundColor: '#fff', borderRadius: 10, padding: 15, marginBottom: 15, shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 5, elevation: 3 },
    username: { fontWeight: 'bold', fontSize: 16, marginBottom: 5, color: '#333' } ,
    caption: { fontSize: 15, marginBottom: 10 },
    image: { width: '100%', height: 250, borderRadius: 8, marginBottom: 10 },
    button: { backgroundColor: "#007AFF", padding: 12, borderRadius: 8, alignItems: 'center', marginTop: 10 },
    buttonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
    input: { backgroundColor: '#fff', borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 10, marginBottom: 15, fontSize: 16 }
});