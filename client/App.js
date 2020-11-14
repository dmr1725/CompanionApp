import { StatusBar } from 'expo-status-bar';
import React, {useState} from 'react';
import { StyleSheet, Text, View } from 'react-native';
import * as Google from "expo-google-app-auth";
import {SocialIcon, socialIcon} from 'react-native-elements'
import {createDrawerNavigator} from '@react-navigation/drawer'
import { NavigationContainer } from '@react-navigation/native';
import * as SecureStore from 'expo-secure-store';

import HomeScreen from './Screens/HomeScreen'
import NotificationsScreen from './Screens/NotificationScreen'
import SettingScreen from './Screens/SettingScreen'
import AddTakenCourses from './Screens/AddTakenCourses'

const Drawer = createDrawerNavigator()

const IOS_CLIENT_ID =
  "116415331974-tf6sehooctplmmn7j0gt831mdf1oqipl.apps.googleusercontent.com";

export default function App() {
  const [hasToken, setHasToken] = useState(false)
  
  const signInWithGoogle = async ()=>{
    try {
      const result = await Google.logInAsync({
        iosClientId: IOS_CLIENT_ID,
        scopes: ["profile", "email"]
      })

      if (result.type == "success"){
        console.log(result.accessToken)

        try {
          let response = await fetch('http://6bbd7a12b6b8.ngrok.io/rest-auth/google/', {
            method: 'POST',
            headers: {
              'content-type': 'application/json'
            }, 
            body: JSON.stringify({
              access_token: `${result.accessToken}`
            })
          })
          let responseJson = await response.json()
          if (responseJson){
            if (responseJson.key){
              await SecureStore.setItemAsync('token', responseJson.key)
            }
          }

        } catch(error){
          console.log(error)
        }
        setHasToken(true) // update states and redirect
      }

      else {
        console.log("no")
      }
    } catch(error){
      console.log(error)
    }
  }
  if (!hasToken){
    return (
      <View style={styles.container}>
        <SocialIcon title="Login With Google" button={true} type={"google"} onPress={signInWithGoogle}/>
      </View>
    );
  }
  console.log(hasToken)
  return (
    <NavigationContainer>
        <Drawer.Navigator initialRouteName="Home">
          <Drawer.Screen name="Home" component={HomeScreen}/>
          <Drawer.Screen name="Notifications" component={NotificationsScreen} />
          <Drawer.Screen name="Settings" component={SettingScreen} />
          <Drawer.Screen name="Add Taken Courses" component={AddTakenCourses} />
        </Drawer.Navigator>
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