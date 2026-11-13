// app/_layout.tsx
// Sion Zhan (sszhan24@bu.edu), 11/12/26
// Defines the root layout wrapper to ensure full screen rendering

import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { View } from 'react-native';

export default function RootLayout() {
  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
      </Stack>
      <StatusBar style="auto" />
    </View>
  );
}