// app/(tabs)/_layout.tsx
// Sion Zhan (sszhan24@bu.edu), 11/12/26
// Defines the tab navigation layout for the dadjokes app

import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    <Tabs screenOptions={{
      tabBarActiveTintColor: 'blue',
      tabBarPosition: 'bottom',
      headerShown: false
    }}>
      <Tabs.Screen name='index' options={{ title: 'Random Joke' }} />
      <Tabs.Screen name='jokes_list' options={{ title: 'Joke List' }} />
      <Tabs.Screen name='add_joke' options={{ title: 'Add Joke' }} />
    </Tabs>
  );
}