import React, {useState, useEffect} from 'react';
import { FlatList, StatusBar, StyleSheet, Text, TouchableOpacity, TextInput, View, Button, ActivityIndicator, Alert, ScrollView, RefreshControl } from "react-native";
import axios from 'axios'
import * as SecureStore from 'expo-secure-store';
import Modal from 'react-native-modal';

const Item = ({ item, onPress, style }) => (
    <TouchableOpacity onPress={onPress} style={[styles.item, style]}>
      <Text style={styles.title}>{`${item.code}`}</Text>
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
    const [animating, setAnimating] = useState(false)
    const [modalVisible, setModalVisible] = useState(false)
    const [code, setCode] = useState(null)
    const [days, setDays] = useState(null)
    const [courseName, setCourseName] = useState(null)
    const [prof, setProf] = useState(null)
    const [rooms, setRooms] = useState(null)
    const [section, setSection] = useState(null)
    const [hours, setHours] = useState(null)
    const [year, setYear] = useState(null)
    const [semestre, setSemestre] = useState(null)

    
    const toggle = ()=>{
        setModalVisible(!modalVisible)
        setSelectedId(null)
    }


    const getMyCurrentCourses = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)

        try {
            let response = await axios(`http://eaff18da08e1.ngrok.io/api/get_current_courses`, {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                    Authorization: `Token ${token}`
                },
                data:{
                    user_id: user_id
                }
            })

            
            if(response.data.list){
                setCourses(response.data.list)
            }
            else{
                setCourses(response.data.msg)
            }
             console.log(courses)
           } catch(error){
               console.log(error)
           }
    }

    const deleteOneCourse = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)
        console.log(semestre)
        console.log(year)

        try {
            let response = await axios(`http://eaff18da08e1.ngrok.io/api/delete_course`, {
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

            getMyCurrentCourses() // get current courses again
            setSection(null)
            setDays(null)
            setHours(null)
            setRooms(null)
            setProf(null)
            
           
           } catch(error){
               console.log(error)
        }

    }

    const onRefresh = React.useCallback(async ()=>{
        setRefreshing(true)
        getMyCurrentCourses()
        setRefreshing(false)

    }, [refreshing])




    useEffect(()=>{
        console.log('dimelo')
        getMyCurrentCourses()
    },[])

    const renderItem = ({ item }) => {
        const backgroundColor = item.id === selectedId ? "#e60505" : "#fafbfc";
        return (
          <Item
            item={item}
            onPress={() => {
              setSelectedId(item.id)
              if(item.section === undefined){
                setCourseName(item.name)
                setCode(item.code)
                setYear(item.year)
                setSemestre(item.semestre)
                setModalVisible(true)
              }
              else{
                setCourseName(item.name)
                setCode(item.code)
                setYear(item.year)
                setSemestre(item.semestre)
                setSection(item.section)
                setDays(item.dias)
                setHours(item.horarios)
                setRooms(item.salones)
                setProf(item.prof)
                setModalVisible(true)
              }
            }}
            style={{ backgroundColor }}
          />
        );
      };

    // if student does not have courses currently, return this
    if(courses === null || courses === 'No tienes cursos'){
        return (
          <ScrollView
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh}/>}
          >
              <Text>No tienes cursos</Text>
          </ScrollView>    
        )
    }
    return (
        <View style={styles.container}>
           <FlatList
                    data={courses}
                    renderItem={renderItem}
                    keyExtractor={(item) => item.id.toString()}
                    extraData={selectedId}
                    ItemSeparatorComponent={renderSeparator}
                    refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh}/>}
            />
            <Modal isVisible={modalVisible} 
            >
            <View style={styles.modalItem}>
                <Text></Text>
                <Text style={styles.course_info}>Name: {courseName}</Text>
                <Text style={styles.course_info}>Code: {code}</Text>
                <Text style={styles.course_info}>{section === null ? '' : 'Section '+ section} </Text>
                <Text style={styles.course_info}>{prof === null ? '' : 'Prof:' + prof} </Text>
                <Text style={styles.course_info}>{days === null ? '' : 'Days: ' + days} </Text>
                <Text style={styles.course_info}>{hours === null ? '' : 'Hours: '+ hours} </Text>
                <Text style={styles.course_info}>{rooms === null ? '' : 'Rooms: ' + rooms} </Text>
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
      height: 270
    },
    course_info: {
        fontWeight: 'bold',
        fontSize: 13
    }
    
  });

// const styles = StyleSheet.create({
//     container: { flex: 1, padding: 16, paddingTop: 30, backgroundColor: '#fff' },
//     head: {  height: 40,  backgroundColor: '#e82020'  },
//     wrapper: { flexDirection: 'row' },
//     title: { flex: 1, backgroundColor: '#e82020' },
//     row: {  height: 28  },
//     text: { textAlign: 'center', fontSize:10 },
//   });