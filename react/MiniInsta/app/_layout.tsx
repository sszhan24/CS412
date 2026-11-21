// _layout.tsx
// Sion Zhan (sszhan24@bu.edu), 11/19/26
// Root layout defining the stack navigation for the MiniInsta app

import { Stack, router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';
import { ActivityIndicator, View } from 'react-native';

export default function RootLayout() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = await AsyncStorage.getItem('userToken');
        const profileId = await AsyncStorage.getItem('profileId');
        // If there's no token, force user to login screen
        if (!token || !profileId) {
          router.replace('/login');
        }
      } catch (error) {
        console.error('Erorr checking auth token: ', error);
      } finally {
        setLoading(false);
      }
    };
    checkAuth();
  }, []);

  // Show a spinner while checking the token
  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size='large' color="#007AFF" />
      </View>
    );
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="login" />
      <Stack.Screen name="(tabs)" />
    </Stack>
  );
}