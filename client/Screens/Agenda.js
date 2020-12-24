import React, {useState, useEffect} from 'react';
import { StyleSheet, View, Text, ScrollView, RefreshControl } from 'react-native';
import WeeklyCalendar from 'react-native-weekly-calendar';
import * as SecureStore from 'expo-secure-store';
import axios from 'axios'

 
export default function App() {
  const [data, setData] = useState('')
  const [sampleEvents, setSampleEvents] = useState([])
  const [refreshing, setRefreshing] = useState(false)
  // const sampleEvents = [
  //   { 'start': '2020-12-06 09:00:00', 'duration': '01:20:00', 'note': 'CCOM4120' },
  //   { 'start': '2020-12-06 14:00:00', 'duration': '01:20:00', 'note': 'MATE3001' },
  //   { 'start': '2020-12-06 17:00:00', 'duration': '00:30:00', 'note': 'INGL1001' },
  //   { 'start': '2020-12-07 14:00:00', 'duration': '02:00:00', 'note': 'SICI3211' },
  //   { 'start': '2020-12-07 10:00:00', 'duration': '02:00:00', 'note': 'BIOL3101' },
  //   { 'start': '2020-12-08 09:00:00', 'duration': '01:20:00', 'note': 'CCOM4120' },
  //   { 'start': '2020-12-08 14:00:00', 'duration': '01:20:00', 'note': 'MATE3001' },
  //   { 'start': '2020-12-08 17:00:00', 'duration': '00:30:00', 'note': 'INGL1001' },
  //   { 'start': '2020-12-09 14:00:00', 'duration': '02:00:00', 'note': 'SICI3211' },
  //   { 'start': '2020-12-09 10:00:00', 'duration': '02:00:00', 'note': 'BIOL3101' },

  // ]

  const getMyCurriculum = async()=>{
    const token = await SecureStore.getItemAsync('token')
    let id = await SecureStore.getItemAsync('id')
    let user_id = parseInt(id)

    let response = await axios({
      method: 'POST',
      url: 'http://a558914af11a.ngrok.io/api/get_current_courses',
      headers: {
        'content-type': 'application/json',
        Authorization: `Token ${token}`
      },
      data: {
        user_id: user_id
      }
    })
    // setSampleEvents([])
    console.log(response.data.list, '------------------------------------------------------------------------------d')

    if(response.data.msg){
      setSampleEvents([])
    }

    else if(response.data.list[0].horarios === undefined){
      setSampleEvents([])

    }

    else {
        // courses
        setData(response.data.list)  
        console.log(data)

        // Loop para ir curso por curso y a~adir a la agenda
        let courses = []
        data.map((course)=>{
          // console.log(typeof(course.horarios))
          
          let horarios = course.horarios
          let titulo = course.name
          let horario_length = horarios.length
          let horas = 0
          let minutos = 0
          let segundos = "00"
          let dura = ""
          let repetir = 0


          let hora =""
          let empieza= ""
          let minuto = ""
          // console.log(horario_length)
          horarios = horarios.replace(/A/g,'')
          horarios = horarios.replace(/M/g,'')
          horarios = horarios.replace(/P/g,'')
          horarios = horarios.replace(/-/g,':')
          // console.log(horarios)

          // Bregando con la DURACION
          if(horario_length == 15){
            horarios = horarios.split(':')
            horas = horarios[2] - horarios[0]
            minutos = horarios[3] - horarios[1]
            minutos = minutos.toString()
            horas = horas.toString()
            horas = '0' + horas
            // console.log("Horas: ", horas)
            // console.log("Minutos: ", minutos)
            // console.log("Segundos: ", segundos)
            dura = horas + ":" + minutos + ":" + segundos
            // console.log(dura)
            // console.log(typeof(segundos))
            // console.log(typeof(dura))
          }
          // Duracion para mas de un horario de una clase
          else{
            horarios = horarios.replace(/,/g,':')
            horarios = horarios.split(':')
            horario_length = horarios.length
            console.log(horario_length)
            repetir = horario_length/4
            console.log("Repetir: ", repetir)
            console.log(horarios)

            horas = horarios[2] - horarios[0]
            minutos = horarios[3] - horarios[1]
            minutos = minutos.toString()
            horas = horas.toString()
            horas = '0' + horas
            // console.log("Horas: ", horas)
            // console.log("Minutos: ", minutos)
            // console.log("Segundos: ", segundos)
            dura = horas + ":" + minutos + ":" + segundos

            // let horas2 = horarios[7] - horarios[5]
            // let minutos2 = horarios[8] - horarios[6]
            // minutos2 = minutos.toString()
            // horas2 = horas.toString()
            // horas2 = '0' + horas
            // // console.log("Horas: ", horas)
            // // console.log("Minutos: ", minutos)
            // // console.log("Segundos: ", segundos)
            // dura2 = horas2 + ":" + minutos2 + ":" + segundos
          }

          // Bregando con el START
          if (horarios[0] < 7){
            // console.log("Es menor: ", horarios[0])
            hora = Number(horarios[0]) + 12
          }
          else{
            hora = horarios[0]
          }
          minuto = horarios[1]
          hora = hora.toString()
          // console.log("Hora: ", hora)
          // console.log(typeof(hora))
          // console.log("Min: ", minuto)
          // console.log(typeof(minuto))
          empieza = hora + ":" + minuto + ":" + segundos

          let date =""
          let i = 0
          let dias = course.dias
          for (i = 0; i < dias.length; i++ ){
            console.log("Esta es la letra ahora: ", dias[i])
            let month_year = "2020-12"
            let date_time = ""

            if(dias[i] == "L"){
              date = "-14 "
              date_time = month_year + date + empieza
              console.log()
              console.log("Starts: ", date_time)
              // console.log("Duracion: ", dura)
              // console.log(typeof(empieza))
              courses.push({start: date_time, duration: dura , note: course.code})
              console.log(dias)
            }

            if(dias[i] == "M"){
              date = "-15 "
              date_time = month_year + date + empieza
              console.log()
              console.log("Starts: ", date_time)
              // console.log("Duracion: ", dura)
              // console.log(typeof(empieza))
              courses.push({start: date_time, duration: dura , note: course.code})
              console.log(dias)
            }

            if(dias[i] == "W"){
              date = "-16 "
              date_time = month_year + date + empieza
              console.log()
              console.log("Starts: ", date_time)
              // console.log("Duracion: ", dura)
              // console.log(typeof(empieza))
              courses.push({start: date_time, duration: dura , note: course.code})
              console.log(dias)
            }

            if(dias[i] == "J"){
              date = "-17 "
              date_time = month_year + date + empieza
              console.log()
              console.log("Starts: ", date_time)
              // console.log("Duracion: ", dura)
              // console.log(typeof(empieza))
              courses.push({start: date_time, duration: dura , note: course.code})
              console.log(dias)
            }

            if(dias[i] == "V"){
              date = "-18 "
              date_time = month_year + date + empieza
              console.log()
              console.log("Starts: ", date_time)
              // console.log("Duracion: ", dura)
              // console.log(typeof(empieza))
              courses.push({start: date_time, duration: dura , note: course.code})
              console.log(dias)
            }
          }
        })

        setSampleEvents(courses)
  }

    // console.log(courses)
  }

  const onRefresh = React.useCallback(async ()=>{
    setRefreshing(true)
    setSampleEvents([])
    getMyCurriculum()
    setRefreshing(false)

}, [refreshing])

  const renderCourses = ()=>{
    console.log(sampleEvents, 'sampleevents')
    if(sampleEvents.length > 0){
      return (
       <View>
          <Text>AGENDA DE LA UNI</Text>
          <WeeklyCalendar events={sampleEvents} style={{ height: 400 }} />
       </View>
      )
    }
    else{
      return (
        <View>
          <Text>No tienes agenda porque todavía no has hecho matricula</Text>
          {/* <WeeklyCalendar events={sampleEvents} style={{ height: 400 }} /> */}
       </View>
      )
    }
  }

  useEffect(()=>{
    getMyCurriculum()
  }, [])
  

  return (

    <ScrollView
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh}/>}
          >
              {renderCourses()}
    </ScrollView>    
  );
}
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  }
});