import axios from "axios";
import React, { useState } from "react";
import { FlatList, StatusBar, StyleSheet, Text, TouchableOpacity, TextInput, View, Button, ActivityIndicator } from "react-native";
import * as SecureStore from 'expo-secure-store';
import Modal from 'react-native-modal';
import {Picker} from '@react-native-community/picker';


const Item = ({ item, onPress, style }) => (
  <TouchableOpacity onPress={onPress} style={[styles.item, style]}>
    <Text style={styles.title}>{item.code}</Text>
  </TouchableOpacity>
);

// separates results, taken from https://stackoverflow.com/questions/60350768/how-to-make-search-bar-with-dropdown-list-in-react-native
const renderSeparator = () => {
    return (
      <View
        style={{
          height: 1,
          width: '100%',
          backgroundColor: '#CED0CE',
        }}
      />
    );
};


const AddTakenCourse = () => {
  const [text, setText] = useState('')
  const [selectedId, setSelectedId] = useState(null);
  const [data, setData] = useState([])
  const [modalVisible, setModalVisible] = useState(false)
  const [grade, setGrade] = useState('A')
  const [year, setYear] = useState('1')
  const [semester, setSemester] = useState('1')
  const [animating, setAnimating] = useState('')

  const toggle = ()=>{
    setModalVisible(!modalVisible)
  }

  const addCourse = async ()=>{
      const token = await SecureStore.getItemAsync('token')
      let id = await SecureStore.getItemAsync('id')
      let user_id = parseInt(id)
      console.log('year', year)
      console.log('semester', semester)
      console.log('grade', grade)


      let response = await axios({
        method: 'POST',
        url: 'http://230cd80ec7d6.ngrok.io/api/add_taken_course',
        headers: {
          'content-type': 'application/json',
          Authorization: `Token ${token}`
        },
        data: {
          semester: semester,
          year: year,
          user_id: user_id,
          grade: grade,
          course_id: selectedId
        }
      })

      console.log(response.data)

      setAnimating(true)

      setTimeout(()=>{
        setAnimating(false)
        setModalVisible(false)
        setSelectedId(null)
        setData([])
      }, 3000)
  }



  const searchCourses = async(text)=>{
      let courses = []
      setText(text)
      const token = await SecureStore.getItemAsync('token')
      const response = await axios({
          method: 'GET',
          url: `http://230cd80ec7d6.ngrok.io/api/find_course?code=${text}`,
          headers: {
            'content-type': 'application/json',
            Authorization: `Token ${token}`
          }

      })
      response.data.list.map((course)=>{
        let oneCourse = {'id': course.id, 'code': course.code}
        courses.push(oneCourse)
      })

      setData(courses)
  }

  const renderItem = ({ item }) => {
    const backgroundColor = item.id === selectedId ? "#e60505" : "#fafbfc";
    return (
      <Item
        item={item}
        onPress={() => {
          setSelectedId(item.id)
          setModalVisible(true)
        }}
        style={{ backgroundColor }}
      />
    );
  };


  return (
    <View style={{flex: 1, padding: 10}}>
       <TextInput
        style={styles.searchBar}
        placeholder="Search for a course that you've taken"
        onChangeText={text=>searchCourses(text)}
        // onChangeText={text=>setText(text)}
      />
      <FlatList
        data={data}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        extraData={selectedId}
        ItemSeparatorComponent={renderSeparator}
      />
      <Modal isVisible={modalVisible} style={{
            backgroundColor: 'white',
            flexDirection: 'row',
            borderRadius: 20,
            margin: 50,
            padding: 10,
        }}>
            <View style={styles.modalItem}>
                <Text>Grade</Text>
                <Picker
                    selectedValue={grade}
                    style={{ width: 50}}
                    onValueChange={(itemValue, itemIndex) => setGrade(itemValue) }>
                    <Picker.Item label="A" value="A" />
                    <Picker.Item label="B" value="B" />
                    <Picker.Item label="C" value="C" />
                    <Picker.Item label="D" value="D" />
                    <Picker.Item label="F" value="F" />
                </Picker>
            </View>
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
           <View style={{flex: 1, justifyContent: 'center'}}>
                <ActivityIndicator size="large" color="0000ff" animating={animating}/>
                <View>
                    <Button title="Submit" onPress={addCourse}/>
                    <Button title="Close" onPress={toggle}/>
                </View>
           </View>
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
  },
  searchBar: {
    height: 40, 
    borderColor: '#000', 
    borderWidth: 1 
  },
  modalItem: {
    // width: '30%', // is 30% of container width
    margin: 8 // 300
}
  
});

export default AddTakenCourse;