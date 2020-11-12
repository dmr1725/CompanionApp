import React, { Component } from "react";
import { Text, View, StyleSheet, Button, ScrollView, Picker, TextInput } from "react-native";


export default class SettingScreen extends Component {
    state = {
        faculty: "naturales"

    }
    render() {

        return(


            <View style={styles.container}>
                <View style={{alignItems: "center", backgroundColor: 'red', marginTop: 30, marginBottom: 150}}>
                    <Text style= {{fontSize: 20, fontWeight: "bold"}}> Profile Settings </Text>
            
                </View>

                <View style={{alignItems: "flex-start", backgroundColor: 'Silver', flex:0}}>
                <Button
                    title="<Back"
                    onPress= {() => this.props.navigation.navigate("Profile")}
                    /> 
                </View>

                <View style={{alignItems: "center",backgroundColor: 'white', flex:0}}>
                    <Text style={{ fontSize: 20}}> Name: </Text>
                    <TextInput style= {{borderColor: "black", borderWidth: 2, width: 250}}>
                    </TextInput>
                    <Button
                        title="Update Name"
                        onPress={this.prueba}
                        />
                    <Text style={{ fontSize: 20}}> Email: </Text>
                    <TextInput style= {{borderColor: "black", borderWidth: 2, width: 250}}>
                    </TextInput>
                    <Button
                        title="Update Email"
                        onPress={this.prueba}
                    /> 

                    <Text style={{ fontSize: 20}}> Student ID: </Text>
                    <TextInput style= {{borderColor: "black", borderWidth: 2, width: 250}}>
                    </TextInput>
                    <Button
                        title="Update Student ID"
                        onPress={this.prueba}
                    /> 
                </View>

                <View style={{alignItems: "center", backgroundColor: 'red', marginTop: 50, marginBottom: 300}}> 
                <Text style={{ fontSize: 20, fontWeight: "bold" , height:30 }}> Faculty </Text>

                    <Picker
                        selectedValue={this.state.faculty}
                        style={{ height: 0, width: 1000}}
                        onValueChange={(itemValue, itemIndex) =>
                        this.setState({ faculty: itemValue })
                        }>
                        
                        <Picker.Item label="Administración de Empresas" value="001" />
                        <Picker.Item label="Arquitectura" value="002" />
                        <Picker.Item label="Ciencias Naturales" value="003" />
                        <Picker.Item label="Ciencias Sociales" value="004" />
                        <Picker.Item label="Educación" value="005" />
                        <Picker.Item label="Bellas Artes" value="006" />
                        <Picker.Item label="Communicaciones" value="007" />
                    </Picker>
                </View>
        </View>
            
        );
    }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center"
  }
  

});

