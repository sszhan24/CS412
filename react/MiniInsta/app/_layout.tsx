// _layout.tsx
// Sion Zhan (sszhan24@bu.edu), 11/19/26
// Root layout defining the stack navigation for the MiniInsta app

import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="login" />
      <Stack.Screen name="(tabs)" />
    </Stack>
  );
}