import { StatusBar } from 'expo-status-bar';
import React, {useState} from 'react';
import { StyleSheet, Text, View } from 'react-native';
import * as Google from "expo-google-app-auth";
import {SocialIcon, socialIcon} from 'react-native-elements'
import {createDrawerNavigator} from '@react-navigation/drawer'
import { NavigationContainer } from '@react-navigation/native';
import * as SecureStore from 'expo-secure-store';

import HomeScreen from './HomeScreen'
import NotificationsScreen from './NotificationScreen'
import SettingScreen from './SettingScreen'
import AddTakenCourse from './AddTakenCourse'
import MyCurriculum from './MyCurriculum'
import EnrollNextSemester from './EnrollNextSemester'
import Logout from './Logout'
import CurrentCourses from './CurrentCourses'
import EditGrades from './EditGrades'
import UpdateSemYear from './UpdateSemYear'


const Drawer = createDrawerNavigator()

const IOS_CLIENT_ID =
  "116415331974-tf6sehooctplmmn7j0gt831mdf1oqipl.apps.googleusercontent.com";

export default function Login() {
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
          // login user in backend
          let response = await fetch('http://41081083853a.ngrok.io/rest-auth/google/', {
            method: 'POST',
            headers: {
              'content-type': 'application/json'
            }, 
            body: JSON.stringify({
              access_token: `${result.accessToken}`
            })
          })

          // storing our token
          let responseJson = await response.json()
          if (responseJson){
            if (responseJson.key){
              await SecureStore.setItemAsync('token', responseJson.key)
            }
          }

          const token = await SecureStore.getItemAsync('token')

          // storing our id
          let id = await fetch('http://41081083853a.ngrok.io/api/get_user_id', {
            method: 'GET',
            headers: {
              'content-type': 'application/json',
              Authorization: `Token ${token}`
            }
          })
          let idJson = await id.json()
          if (idJson){
            if(idJson.user_id){
              idJson = idJson.user_id
              let id = idJson.toString()
              await SecureStore.setItemAsync('id', id)
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

  return (
    <Drawer.Navigator initialRouteName="Home">
      <Drawer.Screen name="Home" component={HomeScreen}/>
      <Drawer.Screen name="Notifications" component={NotificationsScreen} />
      {/* <Drawer.Screen name="Settings" component={SettingScreen} /> */}
      <Drawer.Screen name="Add Taken Courses" component={AddTakenCourse} />
      <Drawer.Screen name="My Curriculum" component={MyCurriculum} />
      <Drawer.Screen name="Enroll Next Semester" component={EnrollNextSemester} />
      <Drawer.Screen name="Update Grades" component={EditGrades} />
      <Drawer.Screen name="Current Courses" component={CurrentCourses} />
      <Drawer.Screen name="Set your semester and year" component={UpdateSemYear} />
      <Drawer.Screen name="Logout" component={Logout} />

   </Drawer.Navigator>
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
