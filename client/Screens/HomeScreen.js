import * as React from 'react';
import { Button, View } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import Axios from 'axios';
import Logout from './Logout'


function HomeScreen({ navigation }) {
  const credentials = async ()=>{
    const token = await SecureStore.getItemAsync('token')
    const id = await SecureStore.getItemAsync('id')
    console.log(token, id)

    let response = await Axios({
      url: 'http://8aab82eb2b3d.ngrok.io/api/hello',
      method: 'GET',
      headers: {
          Authorization: `Token ${token}`
      }
    })

    console.log(response.data.msg)
  }

  
  
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        {/* <Logout/> */}
        <Button
          onPress={() => navigation.navigate('Notifications')}
          title="Go to notifications"
        />
        <Button
          onPress={credentials}
          title="Prueba"
        />
      </View>
    );
}

export default HomeScreen


