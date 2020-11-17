import axios from "axios";
import React, { useState } from "react";
import { FlatList, SafeAreaView, StatusBar, StyleSheet, Text, TouchableOpacity, TextInput, View } from "react-native";
import * as SecureStore from 'expo-secure-store';


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


  const searchCourses = async(text)=>{
      let courses = []
      setText(text)
      const token = await SecureStore.getItemAsync('token')
      const response = await axios({
          method: 'GET',
          url: `http://ef32e7a10841.ngrok.io/api/find_course?code=${text}`,
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
        onPress={() => setSelectedId(item.id)}
        style={{ backgroundColor }}
      />
    );
  };


  console.log(selectedId)
  return (
    <View style={{padding: 10}}>
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
  }
});

export default AddTakenCourse;