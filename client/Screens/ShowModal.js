import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  Button,
  ActivityIndicator
} from "react-native";
import Modal from 'react-native-modal';
import {Picker} from '@react-native-community/picker'

const ShowModal = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [grade, setGrade] = useState('')
  const [year, setYear] = useState('')
  const [semester, setSemester] = useState('')
  const [animating, setAnimating] = useState('')

  const toggle = ()=>{
      setModalVisible(!modalVisible)
  }

  const addCourse = ()=>{
      console.log('grade', grade)
      console.log('year', year)
      console.log('semester', semester)

      setAnimating(true)

      setTimeout(()=>{
        setAnimating(false)
        setModalVisible(false)
      }, 3000)

  }

  return (
    <View style={{flex:1}}>
        <Button title="Show modal" onPress={toggle}/>
        <Modal isVisible={modalVisible} style={{
            backgroundColor: 'white',
            flexDirection: 'row',
            borderRadius: 20,
            margin: 50,
            padding: 10,
        }}>
            <View style={styles.item}>
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
            <View style={styles.item}>
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
            <View style={styles.item}>
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
        flexDirection: 'row',
        flexWrap: 'wrap',
      },
      item: {
        // width: '30%', // is 30% of container width
        margin: 8 // 300
    }
})

// style={{ flex: 1, justifyContent: "center" }} // line 23


export default ShowModal;