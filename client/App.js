import { StatusBar } from 'expo-status-bar';
import React, {useState} from 'react';
import { StyleSheet, Text, View } from 'react-native';
import * as Google from "expo-google-app-auth";
import {SocialIcon, socialIcon} from 'react-native-elements'
import {createDrawerNavigator} from '@react-navigation/drawer'
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import * as SecureStore from 'expo-secure-store';

import Login from './Screens/Login'
import Logout from './Screens/Logout'
import HomeScreen from './Screens/HomeScreen';




export default function App() {
  const Stack = createStackNavigator();
  return (
   <NavigationContainer>
      <Stack.Navigator
        screenOptions={{headerShown: false}}
        initialRouteName = "Login"
    >
        <Stack.Screen name = "Login" component={Login}/>
        <Stack.Screen name = "Logout" component={Logout}/>
     </Stack.Navigator>
   </NavigationContainer>
  )
  
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
