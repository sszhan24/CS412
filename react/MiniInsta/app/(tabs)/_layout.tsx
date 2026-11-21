// _layout.tsx
// Sion Zhan (sszhan24@bu.edu), 11/17/26
// Defines the tab navigation layout for the MiniInsta app

import { Tabs, router } from 'expo-router';
import { View, Text, TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * clears the saved login data and returns the user to the login screen
 */
const handleLogout = async () => {
  await AsyncStorage.multiRemove(['userToken', 'profileId']);
  router.replace('/login');
}

/**
 * The tab navigation layout. 
 * Sets up the feed, profile, and create post tabs
 */

export default function TabLayout() {
  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      <Tabs screenOptions={{ tabBarActiveTintColor: 'blue', tabBarPosition: 'bottom', headerShown: true,
        headerLeft: () => (
          <TouchableOpacity onPress={handleLogout} style={{ marginLeft: 16 }}>
            <Text style={{ color: 'blue', fontSize: 16 }}>Log Out</Text>
          </TouchableOpacity>
        ),
       }}
      >
        <Tabs.Screen name='feed' options={{ title: 'Feed' }} />
        <Tabs.Screen name='profile' options={{ title: 'My Profile' }} />
        <Tabs.Screen name='create_post' options={{ title: 'New Post' }} />
      </Tabs>
    </View>
  );
}