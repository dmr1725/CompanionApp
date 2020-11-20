import React, { useState, useEffect } from "react";
import { Text, View, StyleSheet, Button, ScrollView, TextInput } from "react-native";
import {Picker} from '@react-native-community/picker'
import * as SecureStore from 'expo-secure-store';
import axios from "axios";


export default function SettingScreen() {
    const [currentFaculty, setCurrentFaculty] = useState('') // faculty of backend
    const [faculty, setFaculty] = useState('') // faculty of dropdown

    const getFaculty = async ()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)

       try {
        let response = await axios(`http://a9e3ae82a86e.ngrok.io/api/get_faculty_name?id=${user_id}`, {
            method: 'GET',
            headers: {
                'content-type': 'application/json',
                Authorization: `Token ${token}`
            },
        })
        setCurrentFaculty(response.data.FacultyName[0])
       } catch(error){
           console.log(error)
       }
    }

    useEffect(()=>{
        console.log('dimelooo')
        getFaculty()
    },[currentFaculty])

    const updateFaculty = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = id
        let fac_id = faculty
        // console.log(typeof(fac_id))
        
        try {
            let response = await axios({
                method: 'PATCH',
                url: 'http://a9e3ae82a86e.ngrok.io/api/update_faculty',
                headers: {
                    Authorization: `Token ${token}`
                },
                data: {
                    id: user_id,
                    fac_id_id: fac_id
                }
            })
            console.log(response.data.list)
           } catch(error){
               console.log(error)
        }
        setCurrentFaculty(faculty)
    }
    console.log(faculty)
    return(
        <View style={styles.container}>
            <View style={{textAlignVertical: 'top'}}>
                <Text style={{ fontSize: 12, fontWeight: "bold" , height:30 }}>
                    You currently belong to the faculty: {currentFaculty}
                </Text>
            </View>
            <View style={{alignItems: "center", backgroundColor: 'red', marginTop: 50, marginBottom: 300}}> 
                <Text style={{ fontSize: 20, fontWeight: "bold" , height:30 }}> Faculty </Text>
                <Picker
                    selectedValue={faculty}
                    style={{ height: 0, width: 1000}}
                    onValueChange={(itemValue, itemIndex) => setFaculty(itemValue) }>
                    <Picker.Item label="Administración de Empresas" value="1" />
                    <Picker.Item label="Administración de Empresas Graduado" value="2" />
                    <Picker.Item label="Arquitectura" value="3" />
                    <Picker.Item label="Arquitectura Graduado" value="4" />
                    <Picker.Item label="Asuntos Académicos" value="5" />
                    <Picker.Item label="Ciencias Militares" value="6" />
                    <Picker.Item label="Ciencias Naturales" value="7" />
                    <Picker.Item label="Ciencias Naturales Graduado" value="8" />
                    <Picker.Item label="Ciencias Sociales" value="9" />
                    <Picker.Item label="Ciencias Sociales Graduado" value="10" />
                    <Picker.Item label="Escuela de Comunicación" value="11" />
                    <Picker.Item label="Escuela de Comunicación Graduado" value="12" />
                    <Picker.Item label="Educación" value="13" />
                    <Picker.Item label="Educación Continua (BEOF)" value="14" />
                    <Picker.Item label="Educación Graduada" value="15" />
                    <Picker.Item label="Escuela de Derecho" value="16" />
                    <Picker.Item label="Escuela Graduada de Ciencias y Tecnologías de la Información" value="17" />
                    <Picker.Item label="Estudios Generales" value="18" />
                    <Picker.Item label="Humanidades" value="19" />
                    <Picker.Item label="Humanidades Graduado" value="20" />
                    <Picker.Item label="Planificación" value="21" />
                </Picker>
            </View>
            <Button
                    onPress={updateFaculty}
                    title="Change Faculty"
            />
        </View>
        
    );
    
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center"
  }
  

});

