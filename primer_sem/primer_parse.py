import pandas as pd
import json
from os import remove


def initial_parse(name, url):

    table_MN = pd.read_html(url)
    df = table_MN[0]
    
    df.columns = ['Curso', 'Nombre', 'c', 'Dias', 'Hora', 'Salon']

    upi = df[['Curso', 'Nombre', 'Dias', 'Hora', 'Salon']]
    # print(upi.head())
    # print(upi.to_json(orient='records'))

    # puedes usar esta alternativa o la de la linea 17
    # upi.to_json(r'C:\Users\diego\Documents\miupi_parse\soup\file.json')
    upi.to_json(f'{name}_temp.json', orient='records')


def final_parse(name):

    with open(f"{name}_temp.json") as f_in:
        data = json.load(f_in)

    newdata = {}

   
    for item in data:
        # print(item)
        if(item["Curso"] != None):
            course = item["Curso"][0:8]
            info = item["Nombre"].split("Profesor: ")
            labCourse = course + '_' + 'LAB'

            courseName = info[0]
            creditos = info[1][-1]
           

            if(course in newdata):
                if(newdata[course][0] != courseName):
                    newKey = course + '_' + 'LAB'
                    if(newKey not in newdata):
                        newdata[newKey] = []
                        newdata[newKey].append(courseName)
                        newdata[newKey].append(creditos)
            
            else:
                newdata[course] = []
                newdata[course].append(courseName)
                newdata[course].append(creditos)


    # print(newdata)
    # print(len(newdata))


     

    with open(f'{name}.json', 'w') as f_out:
        json.dump(newdata, f_out)


if __name__ == "__main__":
    faculty_urls = {"Asuntos_Aca": "https://miupi.uprrp.edu/horarios/RBA120_AA.HTML",
                    "Admi": "https://miupi.uprrp.edu/horarios/RBA120_AE.HTML",
                    "Admi_Grad": "https://miupi.uprrp.edu/horarios/RBA120_AE2.HTML",
                    "Arqui": "https://miupi.uprrp.edu/horarios/RBA120_AQ.HTML",
                    "Arqui_Grad": "https://miupi.uprrp.edu/horarios/RBA120_AQ2.HTML",
                    "Escuela_Grad_Ciencia_Tech_Info": "https://miupi.uprrp.edu/horarios/RBA120_CB.HTML",
                    "Ciencias_Militares": "https://miupi.uprrp.edu/horarios/RBA120_CM.HTML",
                    "Ciencias_Naturales": "https://miupi.uprrp.edu/horarios/RBA120_CN.HTML",
                    "Ciencias_Naturales_Grad": "https://miupi.uprrp.edu/horarios/RBA120_CN2.HTML",
                    "Comunicaciones": "https://miupi.uprrp.edu/horarios/RBA120_CP.HTML",
                    "Comunicaciones_Grad": "https://miupi.uprrp.edu/horarios/RBA120_CP2.HTML",
                    "Ciencias_Sociales": "https://miupi.uprrp.edu/horarios/RBA120_CS.HTML",
                    "Ciencias_Sociales_Grad": "https://miupi.uprrp.edu/horarios/RBA120_CS2.HTML	",
                    "Escuela_Derecho": "https://miupi.uprrp.edu/horarios/RBA120_DE.HTML",
                    "Educacion_Continua": "https://miupi.uprrp.edu/horarios/RBA120_EC.HTML",
                    "Educacion": "https://miupi.uprrp.edu/horarios/RBA120_ED.HTML",
                    "Educacion_Grad": "https://miupi.uprrp.edu/horarios/RBA120_ED2.HTML",
                    "Estudios_Generales": "https://miupi.uprrp.edu/horarios/RBA120_EG.HTML",
                    "Humanidades": "https://miupi.uprrp.edu/horarios/RBA120_HU.HTML",
                    "Humanidades_Grad": "https://miupi.uprrp.edu/horarios/RBA120_HU2.HTML",
                    "Planificacion": "https://miupi.uprrp.edu/horarios/RBA120_PL.HTML"}

    for key in faculty_urls:
        initial_parse(key, faculty_urls[key])
        final_parse(key)
        remove(f"{key}_temp.json")
