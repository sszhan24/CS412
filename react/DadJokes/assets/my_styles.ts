// assets/my_styles.ts
// Sion Zhan (sszhan24@bu.edu), 11/12/26
// Defines shared styling rules for all screens in dadjokes app

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#e0e5ec',
        padding: 20,
        paddingTop: 60,
    },
    card: {
        backgroundColor: '#fff',
        borderRadius: 20,
        padding: 20,
        marginBottom: 20,
        borderWidth: 2,
        borderColor: '#000',
    },
    jokeText: {
        fontSize: 24,
        color: '#00008b',
        marginBottom: 10,
    },
    contributorText: {
        fontSize: 16,
        color: '#333',
    },
    image: {
        width: '100%',
        height: 200,
        resizeMode: 'contain',
        marginVertical: 15,
        borderRadius: 10,
    },
    button: {
        backgroundColor: '#007aff',
        padding: 15,
        borderRadius: 10,
        alignItems: 'center',
        marginTop: 10,
    },
    buttonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    input:{
        backgroundColor: '#fff',
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 10,
        padding: 15,
        marginBottom: 15,
        fontSize: 16,
    }
});