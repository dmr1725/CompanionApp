import * as React from 'react';
import { Button, View } from 'react-native';
import * as SecureStore from 'expo-secure-store';


function HomeScreen({ navigation }) {
  const credentials = async ()=>{
    const response = await SecureStore.getItemAsync('token')
    console.log(response)
  }
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
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


