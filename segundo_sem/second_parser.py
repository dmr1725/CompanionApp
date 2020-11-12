import pandas as pd
import json
from os import remove


def initial_parse(name, url):

    table_MN = pd.read_html(url)
    df = table_MN[0]
    del df[5]
    df.columns = ['Curso', 'Nombre', 'c', 'Dias', 'Hora', 'Salon']

    upi = df[['Curso', 'Nombre', 'Dias', 'Hora', 'Salon']]
    # print(upi.head())
    # print(upi.to_json(orient='records'))

    # puedes usar esta alternativa o la de la linea 17
    # upi.to_json(r'C:\Users\diego\Documents\miupi_parse\soup\file.json')
    upi.to_json(f'{name}2_temp.json', orient='records')


def final_parse(name):

    with open(f"{name}2_temp.json") as f_in:
        data = json.load(f_in)

    newdata = {}

   
    for item in data:
        # print(item)
        course = item["Curso"][0:8]
        info = item["Nombre"]
        labCourse = course + '_' + 'LAB'

        if(course in newdata):
            if( (newdata[course][0] != info) and ('Créditos' not in info) and ('Prof.' not in info)):
                newKey = course + '_' + 'LAB'
                if(newKey not in newdata):
                    newdata[newKey] = []
                    newdata[newKey].append(info)
                    if(info == 'LABORATORIO'):
                        newdata[newKey].append(0)
                    elif(info == 'LABORATORIO INTERMED II'):
                        newdata[newKey].append(2)
                    else:
                        newdata[newKey].append(1)


            elif('Prof.' in info):
                pass

            elif('Créditos' in info):
                creditos = info.split()
                if (newdata[course][0] == "INVESTIG NO GRADUADA"):
                    newdata[course].append(int(creditos[0]))
                elif(len(newdata[course]) == 1):
                    newdata[course].append(int(creditos[0]))
        
        else:
            newdata[course] = []
            newdata[course].append(info)

    # print(newdata)
    # print(len(newdata))


     

    with open(f'{name}2.json', 'w') as f_out:
        json.dump(newdata, f_out)


if __name__ == "__main__":
    faculty_urls = {"Asuntos_Aca": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_AA.HTML",
                    "Admi": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_AE.HTML",
                    "Admi_Grad": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_AE2.HTML",
                    "Arqui": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_AQ.HTML",
                    "Arqui_Grad": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_AQ2.HTML",
                    "Escuela_Grad_Ciencia_Tech_Info": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CB.HTML",
                    "Ciencias_Militares": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CM.HTML",
                    "Ciencias_Naturales": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CN.HTML",
                    "Ciencias_Naturales_Grad": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CN2.HTML",
                    "Comunicaciones": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CP.HTML",
                    "Comunicaciones_Grad": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CP2.HTML",
                    "Ciencias_Sociales": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CS.HTML",
                    "Ciencias_Sociales_Grad": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_CS2.HTML	",
                    "Escuela_Derecho": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_DE.HTML",
                    "Educacion_Continua": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_EC.HTML",
                    "Educacion": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_ED.HTML",
                    "Educacion_Grad": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_ED2.HTML",
                    "Estudios_Generales": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_EG.HTML",
                    "Humanidades": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_HU.HTML",
                    "Humanidades_Grad": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_HU2.HTML",
                    "Planificacion": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_PL.HTML"}
    # faculty_urls = {"Generales": "https://miupi.uprrp.edu/horarios/enero-2019/RBA120_EG.HTML"}
   
    for key in faculty_urls:
        initial_parse(key, faculty_urls[key])
        final_parse(key)
        remove(f"{key}2_temp.json")
