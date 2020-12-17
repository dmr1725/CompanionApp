import * as React from 'react';
import { Button, View } from 'react-native';
import * as SecureStore from 'expo-secure-store';

function Logout({ navigation }) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Button onPress={
        ()=>{
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