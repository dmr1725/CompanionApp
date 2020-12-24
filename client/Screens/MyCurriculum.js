import React, {useState, useEffect} from 'react';
import { View, StyleSheet, Text, TouchableOpacity } from 'react-native';
import axios from 'axios'
import { Table, Row, Rows, TableWrapper, Col, Cell } from 'react-native-table-component';
import {Picker} from '@react-native-community/picker'
import * as SecureStore from 'expo-secure-store';


const MyCurriculum = () =>{
    const [year, setYear] = useState(1)
    const [gpa, setGpa] = useState('')
    const [semester, setSemester] = useState(1)
    const [tableHead, setTableHead] = useState(['','Code', 'Title', 'Credits', 'Grade'])
    const [tableData, setTableData] = useState([])
    const [tableTitle, setTableTitle] = useState([])

    const getMyGPA = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)

        try {
            let response = await axios('http://a558914af11a.ngrok.io/api/see_gpa', {
                method: 'POST',
                headers: {
                    Authorization: `Token ${token}`
                },
                data: {
                    user_id: user_id
                }
            })
            setGpa(response.data["gpa"][0])
        } catch(e){
            console.log(e)
        }
    }

    const getMyCurriculum = async()=>{
        const token = await SecureStore.getItemAsync('token')
        let id = await SecureStore.getItemAsync('id')
        let user_id = parseInt(id)
        let courses = []
        let numbers = []

        try {
            let response = await axios(`http://a558914af11a.ngrok.io/api/get_all_courses_by_semester?user_id=${user_id}&year=${year}&semestre=${semester}`, {
                method: 'GET',
                headers: {
                    'content-type': 'application/json',
                    Authorization: `Token ${token}`
                },
            })
            response = response.data.list // javaScript object

            // setting a column with numbers
            for (let i = 1; i < response.length + 1; i++){
                numbers.push(i)
            }
            setTableTitle(numbers)
            
            // convert javascript array of objects to a javascript 2d array
            response.map((data)=>{
                let info = [data.code, data.name, data.creditos, data.grade]
                courses.push(info)

            })
            setTableData(courses)
           } catch(error){
               console.log(error)
           }
    }




    useEffect(()=>{
        console.log('dimelo')
        getMyCurriculum()
        getMyGPA()
    }, [year, semester, gpa])


    return (
        <View style={styles.container}>
            <Text>Total GPA: {gpa}</Text>
            <Table borderStyle={{borderWidth: 2, borderColor: '#0f0f0f'}}>
                <Row data={tableHead} flexArr={[0.9, 3.5, 10, 2.3, 2.3]} style={styles.head} textStyle={styles.text}/>
                <TableWrapper style={styles.wrapper}>
                    <Col data ={tableTitle} style={styles.title} heightArr={[28,28]} textStyle={styles.text}/>
                    <Rows data={tableData} flexArr={[3.5,10,2.3,2.3]} style={styles.row} textStyle={styles.text} />

                </TableWrapper>
            </Table>
            <View style={{flexDirection: 'row'}}>
                <View style={{margin: 8}}>
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
                <View style={{margin: 8}}>
                    <Text>Semester</Text>
                    <Picker
                            selectedValue={semester}
                            style={{ width: 50}}
                            onValueChange={(itemValue, itemIndex) => setSemester(itemValue) }>
                            <Picker.Item label="1" value="1" />
                            <Picker.Item label="2" value="2" />
                            <Picker.Item label="3" value="3" />
                    </Picker>
                </View>
            </View>
        </View>
    );
}

export default MyCurriculum

const styles = StyleSheet.create({
    container: { flex: 1, padding: 16, paddingTop: 30, backgroundColor: '#fff' },
    head: {  height: 40,  backgroundColor: '#e82020'  },
    wrapper: { flexDirection: 'row' },
    title: { flex: 1, backgroundColor: '#e82020' },
    row: {  height: 28  },
    text: { textAlign: 'center', fontSize:10 },
  });