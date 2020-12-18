import React, {useState, useEffect} from 'react';
import { FlatList, StatusBar, StyleSheet, Text, TouchableOpacity, TextInput, View, Button, ActivityIndicator, Alert, ScrollView, RefreshControl } from "react-native";
import axios from 'axios'
import * as SecureStore from 'expo-secure-store';
import Modal from 'react-native-modal';
import {Picker} from '@react-native-community/picker';

const Item = ({ item, onPress, style }) => (
    <TouchableOpacity onPress={onPress} style={[styles.item, style]}>
      <Text style={styles.title}>{`${item.code}: ${item.grade}`}</Text>
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



const CurrentCourses = () =>{
    const [courses, setCourses] = useState(null)
    const [refreshing, setRefreshing] = useState(false)
    const [selectedId, setSelectedId] = useState(null); // course_id
    const [animating, setAnimating] = useState('')
    const [modalVisible, setModalVisible] = useState(false)
    const [year, setYear] = useState(null)
    const [semestre, setSemestre] = useState(null)
    const [grade, setGrade] = useState('A')

    
    const toggle = ()=>{
        setModalVisible(!modalVisible)
        setSelectedId(null)
    }


    const getAllMyCourses = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)
        console.log(user_id)

        try {
            let response = await axios(`http://41081083853a.ngrok.io/api/get_all_courses_user_has_taken?user_id=${user_id}`, {
                method: 'GET',
                headers: {
                    'content-type': 'application/json',
                    Authorization: `Token ${token}`
                }
            })

            // console.log(response.data.list)
            setCourses(response.data.list)

           } catch(error){
               console.log(error)
           }
    }

    const deleteOneCourse = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)

        try {
            let response = await axios(`http://41081083853a.ngrok.io/api/delete_course`, {
                method: 'DELETE',
                headers: {
                    'content-type': 'application/json',
                    Authorization: `Token ${token}`
                },
                data:{
                    user_id: user_id,
                    course_id: selectedId,
                    year: year,
                    semestre: semestre
                }
            })

            setAnimating(true)
      
            // after 3 seconds, the courses, the modal and the activity indicator will disappear
            setTimeout(()=>{
                setAnimating(false)
                setModalVisible(false)
                setSelectedId(null)
            }, 3000)

            setTimeout(()=>{
                Alert.alert(response.data.msg)
            }, 5000) 

            getAllMyCourses() // get current courses again
            
            
           
           } catch(error){
               console.log(error)
        }

    }

    const updateGrade = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)
        console.log(semestre)
        console.log(year)

        try {
            let response = await axios(`http://41081083853a.ngrok.io/api/update_grade_and_gpa`, {
                method: 'PATCH',
                headers: {
                    'content-type': 'application/json',
                    Authorization: `Token ${token}`
                },
                data:{
                    user_id: user_id,
                    course_id: selectedId,
                    year: year,
                    semestre: semestre,
                    grade: grade
                }
            })

            setAnimating(true)
      
            // after 3 seconds, the courses, the modal and the activity indicator will disappear
            setTimeout(()=>{
                setAnimating(false)
                setModalVisible(false)
                setSelectedId(null)
            }, 3000)

            setTimeout(()=>{
                Alert.alert(response.data.msg)
            }, 5000) 

            getAllMyCourses() // get current courses again
            
            
           
           } catch(error){
               console.log(error)
        }

    }

    const onRefresh = React.useCallback(async ()=>{
        setRefreshing(true)
        getAllMyCourses()
        setRefreshing(false)

    }, [refreshing])




    useEffect(()=>{
        getAllMyCourses()
    },[])

    const renderItem = ({ item }) => {
        const backgroundColor = item.course_id === selectedId ? "#e60505" : "#fafbfc";
        return (
          <Item
            item={item}
            onPress={() => {
              setModalVisible(true)
              setSelectedId(item.course_id)
              setYear(item.year)
              setSemestre(item.semestre)
              setGrade(item.grade)
            }}
            style={{ backgroundColor }}
          />
        );
      };

    // if student does not have courses currently, return this
    if(courses === null || courses.length === 0){
        return (
            <ScrollView
            refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh}/>}
            >
                <Text>No tienes cursos</Text>
            </ScrollView>    
        )
    }
    // console.log(grade)
    return (
        <View style={styles.container}>
           <FlatList
                    data={courses}
                    renderItem={renderItem}
                    keyExtractor={(item) => item.course_id.toString()}
                    extraData={selectedId}
                    ItemSeparatorComponent={renderSeparator}
                    refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh}/>}
            />
            <Modal isVisible={modalVisible} 
            >
            <View style={styles.modalItem}>
                <Button title= "Update grade" onPress={updateGrade} />
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
                <ActivityIndicator size="small" color="0000ff" animating={animating}/>
                <Button title="Delete Course" onPress={deleteOneCourse}/>
                <Button title="Close" onPress={toggle}/>
            </View>
        </Modal>
            

        </View>
    );
}

export default CurrentCourses

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
      height: 340
    },
    course_info: {
        fontWeight: 'bold',
        fontSize: 13
    }
    
  });

