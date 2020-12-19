import axios from "axios";
import React, { useState, useEffect } from "react";
import { StatusBar, StyleSheet, Text, View, Button, Alert } from "react-native";
import * as SecureStore from 'expo-secure-store';
import Modal from 'react-native-modal';
import {Picker} from '@react-native-community/picker';



const UpdateSemYear = () => {
  
  const [year, setYear] = useState('1')
  const [semester, setSemester] = useState('1')
  const [modalVisible, setModalVisible] = useState(false)
  
    const updateSemesterAndYear = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)
    

        let response = await axios({
        method: 'PATCH',
        url: 'http://eaff18da08e1.ngrok.io/api/update_year_and_semester',
        headers: {
            'content-type': 'application/json',
            Authorization: `Token ${token}`
        },
        data: {
            user_id: user_id,
            year: year,
            semester: semester
        }
        })
        console.log(response.data)

        getSemesterAndYear()
        toggle()

    }
 

  const getSemesterAndYear = async ()=>{
      const token = await SecureStore.getItemAsync('token')
      let id = await SecureStore.getItemAsync('id')
      let user_id = parseInt(id)
     

      let response = await axios({
        method: 'POST',
        url: 'http://eaff18da08e1.ngrok.io/api/get_year_and_semester',
        headers: {
          'content-type': 'application/json',
          Authorization: `Token ${token}`
        },
        data: {
          user_id: user_id,
        }
      })

      setYear(response.data.msg.year)
      setSemester(response.data.msg.semestre)


  }

  const toggle = ()=>{
    setModalVisible(!modalVisible)
  }

  useEffect(()=>{
    getSemesterAndYear()
},[])


  console.log(year)
  return (
    <View style={{flex: 1, padding: 10}}>
       <Text style={styles.title}>Your current year is {year} and current semester is {semester}</Text>
       <Button title="Change Year and Semester" onPress={toggle}/>
       <Modal 
            isVisible={modalVisible}
        >
        <View style={styles.modalItem}>
                    <Text>Year</Text>
                    <Picker
                        selectedValue={year}
                        style={{ width: 50}}
                        onValueChange={(itemValue, itemIndex) => setYear(itemValue) }>
                        <Picker.Item label="1" value="1" />
                        <Picker.Item label="2" value="2" />
                        <Picker.Item label="3" value="3" />
                        <Picker.Item label="4" value="4" />
                        <Picker.Item label="5" value="5" />
                        <Picker.Item label="6" value="6" />
                    </Picker>
                </View>
                <View style={styles.modalItem}>
                    <Text>Semester</Text>
                    <Picker
                        selectedValue={semester}
                        style={{ width: 50}}
                        onValueChange={(itemValue, itemIndex) => setSemester(itemValue) }>
                        <Picker.Item label="1" value="1" />
                        <Picker.Item label="2" value="2" />
                    </Picker>
            </View>
            <Button title="Submit" onPress={updateSemesterAndYear}/>
            <Button title="Close" onPress={toggle}/>

       </Modal>
    </View>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: StatusBar.currentHeight || 0,
  },
  item: {
    padding: 10,
    marginVertical: 8,
    marginHorizontal: 16,
  },
  title: {
    fontSize: 15,
    fontWeight: 'bold'
  },
  searchBar: {
    height: 40, 
    borderColor: '#000', 
    borderWidth: 1 
  },
  modalItem: {
    // width: '30%', // is 30% of container width
    margin: 8, // 300
    backgroundColor: 'white'
}
  
});

export default UpdateSemYear;