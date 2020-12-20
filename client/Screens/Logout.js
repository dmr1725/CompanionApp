import * as React from 'react';
import { Button, View } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import Axios from 'axios';

function Logout({ navigation }) {

  const backendLogout = async()=>{
      const token = await SecureStore.getItemAsync('token')
      
      let response = await Axios({
        method: 'POST',
        url: 'http://495f15964a0a.ngrok.io/api/logout',
        headers: {
          'content-type': 'application/json',
          Authorization: `Token ${token}`
        }
      })
      console.log(response.data)
  }

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Button onPress={
        ()=>{
          backendLogout()
          SecureStore.deleteItemAsync('token')
          SecureStore.deleteItemAsync('id')
          navigation.push('Login')

        }
      } title="LOGOUT" />
    </View>
  );
}
export default Logout

// navigation.navigate('Login', {screen: 'Login'})