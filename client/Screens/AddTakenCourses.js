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
                    <Text style= {{fontSize: 20, fontWeight: "bold"}}> Add Taken </Text>
                    <Text style= {{fontSize: 20, fontWeight: "bold"}}>Course{/*{this.props.navigation.getParam("username")} */}</Text>

                </View>

                <View style={{alignItems: "flex-start", backgroundColor: 'white', flex:0}}>
                <Button
                    title="<Back"
                    onPress= {() => this.props.navigation.navigate("Profile")}
                    /> 
                </View>

                <View style={{alignItems: "flex-start",backgroundColor: 'white', flex:0}}>
                    <Text style={{ fontSize: 20}}> Course: </Text>
                    <TextInput style= {{borderColor: "black", borderWidth: 2, width: 100}}>
                    </TextInput>
                    
                    <Text style={{ fontSize: 20}}> Section: </Text>
                    <TextInput style= {{borderColor: "black", borderWidth: 2, width: 100}}>
                    </TextInput>

                    <Text style={{ fontSize: 20}}> Semester#: </Text>
                    <TextInput style= {{borderColor: "black", borderWidth: 2, width: 100}}>
                    </TextInput>

                    <Text style={{ fontSize: 20}}> Professor: </Text>
                    <TextInput style= {{borderColor: "black", borderWidth: 2, width: 250}}>
                    </TextInput>
                </View>

                <View style={{alignItems: "flex-end", backgroundColor: 'white', marginTop: 50, marginBottom: 250}}> 
                <Text style={{ fontSize: 20, fontWeight: "bold" , height:30 }}> Grade: </Text>
                    <Picker
                    selectedValue={this.state.faculty}
                    style={{ height: 0, width: 40}}
                    onValueChange={(itemValue, itemIndex) =>
                    this.setState({ faculty: itemValue })}>
                        <Picker.Item label="A" value="001" />
                        <Picker.Item label="B" value="002" />
                        <Picker.Item label="C" value="003" />
                        <Picker.Item label="D" value="004" />
                        <Picker.Item label="F" value="005" />
                        <Picker.Item label="PS" value="006" />
                        <Picker.Item label="NP" value="007" />
                    </Picker>
                </View>
                    <Button
                        title="Submit Taken Course"
                        onPress={null}
                    /> 
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

