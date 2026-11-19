// _layout.tsx
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Defines the tab navigation layout for the MiniInsta app

import { Tabs } from 'expo-router';
import { View } from 'react-native';

/**
 * The tab navigation layout. 
 * Sets up the feed, profile, and create post tabs
 */

export default function TabLayout() {
  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      <Tabs screenOptions={{ tabBarActiveTintColor: 'blue', tabBarPosition: 'bottom', headerShown: false }}>
        <Tabs.Screen name='feed' options={{ title: 'Feed' }} />
        <Tabs.Screen name='profile' options={{ title: 'My Profile' }} />
        <Tabs.Screen name='create_post' options={{ title: 'New Post' }} />
      </Tabs>
    </View>
  );
}