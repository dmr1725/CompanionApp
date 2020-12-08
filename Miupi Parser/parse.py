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

    newdata = []

    for item in data:
        if(item["Curso"] == None):
            pass
        else:
            course = {}
            course["Curso"] = item["Curso"][0:8]
            course["Seccion"] = item["Curso"][9:12]

            info = item["Nombre"].split("Profesor: ")
            if((profesor := info[1][0:-11]) != ""):
                course["Profesor"] = profesor
            else:
                course["Profesor"] = "TBA"
            
            course["Creditos"] = info[1][-1]
            course["Nombre"] = info[0][0:-1]

            # bregando con dias
            days = item["Dias"].split(" ")
            for i in range(len(days)):
                if i == 0:
                    course["Dias"] = days[i]
                else:
                    course["Dias"] = course["Dias"] + ',' + days[i]

            # si la clase es lab, conferencia o taller
            if course["Nombre"] == 'CONFERENCIA' or course["Nombre"] == 'LABORATORIO' or course['Nombre'] == 'TALLER':
                course["Curso"] += '_LAB'


            
            # bregando con el horario
            if(item["Hora"] != None):
                if len(item["Hora"]) == 15:
                    course["Horario"] = item["Hora"]
                else:
                    course["Horario"] = item["Hora"][0:15] + ',' + item["Hora"][15:30]
            else:
                course["Horario"] = "TBA"
            

            # bregando con salones
            salones_raw = item["Salon"].split("Edificio: ")
            salones = []
            for i in salones_raw:
                if(i != "-" and i != "- " and i != ""):
                    salones.append(i[:-1])
            # una vez los tenga en un array, los voy a unir con una comma para poder insertarlos a la base de datos como datatype string
            if len(salones) == 0:
                course["Salones"] = "TBA"
            else:
                for i in range(len(salones)):
                    if i == 0:
                        course["Salones"] = salones[i]
                    else:
                        course["Salones"] = course["Salones"] + ',' + salones[i]
            
            print(course["Salones"])
                

            

            newdata.append(course)

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
    #initial_parse("Naturales", faculty_urls["Naturales"])
    for key in faculty_urls:
        initial_parse(key, faculty_urls[key])
        final_parse(key)
        remove(f"{key}_temp.json")