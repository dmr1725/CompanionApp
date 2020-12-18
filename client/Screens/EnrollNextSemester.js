import axios from "axios";
import React, { useState } from "react";
import { FlatList, StatusBar, StyleSheet, Text, TouchableOpacity, TextInput, View, Button, ActivityIndicator, Alert } from "react-native";
import * as SecureStore from 'expo-secure-store';
import Modal from 'react-native-modal';


const Item = ({ item, onPress, style }) => (
  <TouchableOpacity onPress={onPress} style={[styles.item, style]}>
    <Text style={styles.title}>{`${item.code}-${item.section}`}</Text>
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


const EnrollNextSemester = () => {
  const [text, setText] = useState('')
  const [selectedId, setSelectedId] = useState(null);
  const [data, setData] = useState([])
  const [modalVisible, setModalVisible] = useState(false)
  const [animating, setAnimating] = useState('')
  const [isSummer, setIsSummer] = useState('false')
  const [code, setCode] = useState('')
  const [creditos, setCreditos] = useState('')
  const [days, setDays] = useState('')
  const [courseName, setCourseName] = useState('')
  const [prof, setProf] = useState('')
  const [rooms, setRooms] = useState('')
  const [section, setSection] = useState('')
  const [hours, setHours] = useState('')

  const toggle = ()=>{
    setModalVisible(!modalVisible)
    setSelectedId(null)
  }

  // add course (enroll) to your next semester
  const enrollCourse = async ()=>{
      const token = await SecureStore.getItemAsync('token')
      let id = await SecureStore.getItemAsync('id')
      let user_id = parseInt(id)


      let response = await axios({
        method: 'POST',
        url: 'http://41081083853a.ngrok.io/api/matricular_prox_semestre',
        headers: {
          'content-type': 'application/json',
          Authorization: `Token ${token}`
        },
        data: {
          user_id: user_id,
          course_id: selectedId,
          isSummer: isSummer
        }
      })
      console.log(response.data.msg)
    //   setMsg(response.data.msg)

      setAnimating(true)
      
      // after 3 seconds, the courses, the modal and the activity indicator will disappear
      setTimeout(()=>{
        setAnimating(false)
        setModalVisible(false)
        setSelectedId(null)
        setData([]) // courses will disappear because data would be empty
      }, 3000)

      setTimeout(()=>{
          Alert.alert(response.data.msg)
      }, 5000)

  }



  const searchCourses = async(text)=>{
      let courses = []
      setText(text)
      const token = await SecureStore.getItemAsync('token')
      const response = await axios({
          method: 'GET',
          url: `http://41081083853a.ngrok.io/api/select_course_prox_semestre?code=${text}`,
          headers: {
            'content-type': 'application/json',
            Authorization: `Token ${token}`
          }

      })
      // looping through our response data and creating a course object to append it to the courses array
      response.data.list.map((course)=>{
        let oneCourse = {'id': course.id, 'name': course.name,'code': course.code, 'creditos': course.creditos, 'prof': course.prof, 'section': course.section, 'hours': course.hours, 'days': course.days, 'rooms': course.rooms}
        courses.push(oneCourse)
      })

      setData(courses)
    //   console.log(courses)
  }

  const renderItem = ({ item }) => {
    const backgroundColor = item.id === selectedId ? "#e60505" : "#fafbfc";
    return (
      <Item
        item={item}
        onPress={() => {
          setSelectedId(item.id)
          setCourseName(item.name)
          setCode(item.code)
          setCreditos(item.creditos)
          setSection(item.section)
          setDays(item.days)
          setHours(item.hours)
          setRooms(item.rooms)
          setProf(item.prof)
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
        placeholder="Search for a course that you want to enroll for next semester"
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
      <Modal isVisible={modalVisible} 
        >
            <View style={styles.modalItem}>
                <Text></Text>
                <Text style={styles.course_info}>Name: {courseName}</Text>
                <Text style={styles.course_info}>Code: {code}</Text>
                <Text style={styles.course_info}>Credits: {creditos}</Text>
                <Text style={styles.course_info}>Section: {section}</Text>
                <Text style={styles.course_info}>Prof: {prof}</Text>
                <Text style={styles.course_info}>Days: {days}</Text>
                <Text style={styles.course_info}>Hours: {hours}</Text>
                <Text style={styles.course_info}>Rooms: {rooms}</Text>
                <ActivityIndicator size="small" color="0000ff" animating={animating}/>
                <Button title="Enroll" onPress={enrollCourse}/>
                <Button title="Close" onPress={toggle}/>
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
    margin: 60, // 300
    backgroundColor: 'white',
    borderRadius:20,
    height: 270
  },
  course_info: {
      fontWeight: 'bold',
      fontSize: 13
  }
  
});

export default EnrollNextSemester;