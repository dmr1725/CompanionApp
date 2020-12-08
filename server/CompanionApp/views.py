import sys
import json
sys.path.insert(1,'C:/Users/diego/Documents/companion_app_gh/organizar/')


from organizar import files3, proxSemFiles


from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from django.db import connection

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import Facultad, Curso, ProximoSemestre
from .serializers import FacultadSerializer, CursoSerializer
from rest_framework.decorators import api_view

# clientID: 965339169610-8et02d4qpfk96vclngd0otths1rs8661.apps.googleusercontent.com
# clientSecret: zeY8NoW6ORBHP8pDQLE2x_Z2

# Create your views here.

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

@api_view(['POST',])
def insertarFacultades(request):
    faculties = [ 'Administración de Empresas', 'Administración de Empresas graduado', 'Arquitectura', 'Arquitectura Graduado', 'Asuntos Académicos',
    'Ciencias Militares', 'Ciencias Naturales', 'Ciencias Naturales Graduado', 'Ciencias Sociales', 'Ciencias Sociales Graduado',
    'Escuela de Comunicación', 'Escuela de Comunicación Graduada', 'Educación', 'Educación Continua (BEOF)', 'Educación Graduado',
    'Escuela de Derecho', 'Escuela Graduada de Ciencias y Tecnologías de la Información', 'Estudios Generales', 'Humanidades',
    'Humanidades Graduado', 'Planificación']
    if request.method == 'POST':
        for faculty in faculties:
            facultad_serializer = FacultadSerializer(data={'fname': faculty})
            if facultad_serializer.is_valid():
                facultad_serializer.save()
        
        return JsonResponse({"message": 'se crearon todas las facultades'}, status=status.HTTP_201_CREATED)

@api_view(['POST',])
def insertarTodosLosCursos(request):
    if request.method == 'POST':
        i = 1
        for file in files3:
            check = file['file'].split('.')
            path = "C:/Users/diego/Documents/companion_app_gh/segundo_sem" if check[0][-1] == '2' else "C:/Users/diego/Documents/companion_app_gh/primer_sem"
            with open(path + '/' + file['file']) as f:
                data = json.load(f)
                fac_id = file['num']
                for key in data:
                    if key != 'Horario ':
                        code = key
                        name = data[key][0]
                        creds = data[key][1]
                        # si la clase es un laboratorio de 0 creditos
                        if 'LAB' in key and (name == 'LABORATORIO' or name == 'LABORATORIO ' or name == 'TALLER' or name == 'TALLER ' or name == 'CONFERENCIA' or name == 'CONFERENCIA '):
                            creds = 0
                            try: 
                                curso = Curso.objects.get(code = code)
                            except Curso.DoesNotExist:
                                curso = None

                            if curso == None:
                                curso_serializer = CursoSerializer(data={'name': name, 'code': code, 'creditos': creds, 'fac_id': fac_id})
                                if curso_serializer.is_valid():
                                    curso_serializer.save()
                            else:
                                print('ya se creo del lab', i)
                                i += 1
                        elif 'LAB in key' and (name != 'LABORATORIO' or name != 'LABORATORIO ' or name != 'TALLER' or name != 'TALLER ' or name != 'CONFERENCIA' or name != 'CONFERENCIA '):
                            continue
                        
                        # todas las otras clases que no tengan _LAB en su codigo
                        else:
                            try: 
                                curso = Curso.objects.get(code = code)
                            except Curso.DoesNotExist:
                                curso = None
                            
                            if curso == None:
                                curso_serializer = CursoSerializer(data={'name': name, 'code': code, 'creditos': creds, 'fac_id': fac_id})
                                if curso_serializer.is_valid():
                                    curso_serializer.save()
                            else:
                                print('ya se creo', i)
                                i += 1
        return JsonResponse({'message': 'se insertaron todos los cursos'}, status=status.HTTP_201_CREATED)

@api_view(['POST',])
def insertarTodosLosCursosProxSemestre(request):
    if request.method == 'POST': 
        for file in proxSemFiles:
            path = "C:/Users/diego/Documents/companion_app_gh/Miupi Parser"
            with open(path + '/' + file['file']) as f:
                data = json.load(f)
                fac_id = file["num"] # this id comes from the file organizar. If the course does not exist in table Curso, use this id
                for course in data:
                    name = course["Nombre"]
                    code = course["Curso"]
                    creditos = int(course["Creditos"])
                    section = course["Seccion"]
                    prof = course["Profesor"]
                    hours = course["Horario"]
                    days = course["Dias"]
                    rooms = course["Salones"]


                    # seeing if course from json file already exists in table Curso
                    cursor = connection.cursor()
                    cursor.execute(f'SELECT id from "CompanionApp_curso" where code = \'{code}\'')
                    course_id = cursor.fetchone()

                    # if course does not exist in table Curso, create the course in table Course and create the course in table ProximoSemestre
                    if course_id == None:
                        # create course
                        cursor = connection.cursor()
                        cursor.execute(f'INSERT INTO "CompanionApp_curso" (name, code, creditos, fac_id_id) VALUES (\'{name}\', \'{code}\', {creditos}, {fac_id})')
                        
                         # seeing again if course from json file already exists in table Curso to fetch course_id
                        cursor = connection.cursor()
                        cursor.execute(f'SELECT id from "CompanionApp_curso" where code = \'{code}\'')
                        course_id = cursor.fetchone()
                       
                  
                    # insert course to the table ProxSemestre
                    course_id = course_id[0]
                    cursor = connection.cursor()
            
                    cursor.execute(f'INSERT INTO "CompanionApp_proximosemestre" (name, code, creditos, section, prof, hours, days, rooms, course_id_id) VALUES (\'{name}\', \'{code}\', {creditos}, \'{section}\', \'{prof}\', \'{hours}\', \'{days}\', \'{rooms}\', {course_id})')
          
        return JsonResponse({'message': 'se insertaron todos los cursos'}, status=status.HTTP_201_CREATED)


@api_view(['PATCH',])
def updateFaculty(request):
    if request.method == 'PATCH':
        # params from request
        fac_id = int(request.data['fac_id_id'])
        user_id = int(request.data['id'])
        print(type(fac_id))
        print('backend', fac_id)

        # update faculty
        cursor = connection.cursor()
        cursor.execute(f'UPDATE "CompanionApp_user" set fac_id_id = {fac_id} where id = {user_id}')
        return JsonResponse({'list': 'updated'}, status=status.HTTP_201_CREATED)


# find courses in our Curso table
@api_view(['GET',])
def findCourse(request):
    # alternative to .filter
    # cursor = connection.cursor()
    # cursor.execute(f'SELECT id, code from "CompanionApp_curso" where code LIKE \'{course_code}%\' LIMIT 10')
    # courses = cursor.fetchall()
    if request.method == 'GET':
        course_code = request.query_params['code'].upper()
        courses = Curso.objects.filter(code__contains=course_code)[:10]
        courses = list(courses.values())
        return JsonResponse({'list': courses}, status=status.HTTP_200_OK)

# find courses in our ProximoSemestre table
@api_view(['GET',])
def selectCourseProxSemestre(request):
    if request.method == 'GET':
        course_code = request.query_params['code'].upper()
        courses = ProximoSemestre.objects.filter(code__contains=course_code)[:10]
        courses = list(courses.values())
        return JsonResponse({'list': courses}, status=status.HTTP_200_OK)


@api_view(['POST'])
def addTakenCourse(request):
    if request.method == 'POST':
        # request params
        user_id = int(request.data['user_id'])
        course_id = int(request.data['course_id'])
        grade = request.data['grade'].upper()
        year = int(request.data['year'])
        semester = int(request.data['semester'])
        repeating = False
        

        # set point of grade
        points = 0
        if grade == 'A':
            points = 4
        elif grade == 'B':
            points = 3
        elif grade == 'C':
            points = 2
        elif grade == 'D':
            points = 1
        elif grade == 'F':
            points = 0
        else:
            return JsonResponse({'msg': 'Insert A, B, C, D or F' }, status=status.HTTP_406_NOT_ACCEPTABLE)

        # find course credits
        cursor = connection.cursor()
        cursor.execute(f'Select creditos from "CompanionApp_curso" where id = {course_id} ')
        course = cursor.fetchone()
        creditos = int(course[0])

        # check if student already took that class in the same year and semester he/she is trying to post
        cursor = connection.cursor()
        cursor.execute(f'select semestre, year, grade, course_id_id from "CompanionApp_matricula" where semestre = {semester} and year = {year} and course_id_id = {course_id} and user_id_id = {user_id}')
        check = cursor.fetchone()
        if check != None:
            check = list(check)
            if int(check[0]) == semester and int(check[1]) == year and check[3] == course_id:
                return JsonResponse({'msg': 'You already took the course that year and semester.' }, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif int(check[1]) != year:
                pass
            elif int(check[1] == year) and int(check[0]) != semester:
                pass
            
        # matricular al estudiante
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO "CompanionApp_matricula" (semestre, year, grade, user_id_id, course_id_id) VALUES ({semester}, {year}, \'{grade}\', {user_id}, {course_id})')

        # find credits taken
        cursor = connection.cursor()
        cursor.execute(f'Select credits_taken from "CompanionApp_user" where id={user_id}')
        credits_taken = cursor.fetchone()
        credits_taken = int(credits_taken[0])

        # find last credits_taken_score
        cursor = connection.cursor()
        cursor.execute(f'Select credits_taken_score from "CompanionApp_user" where id={user_id}')
        credits_taken_score = cursor.fetchone()
        credits_taken_score = int(credits_taken_score[0])

        # update credits taken
        credits_taken += creditos
        cursor = connection.cursor()
        cursor.execute(f'UPDATE "CompanionApp_user" set credits_taken = {credits_taken} where id ={user_id}')

        # update credits_taken_score
        credits_taken_score = credits_taken_score + (creditos * points)
        cursor = connection.cursor()
        cursor.execute(f'UPDATE "CompanionApp_user" set credits_taken_score = {credits_taken_score} where id ={user_id}')

 
        # set GPA and insert it in user
        credit_score = credits_taken * 4
        gpa = (credits_taken_score / credit_score) * 4.0
        gpa = float("{:.2f}".format(gpa))
        cursor = connection.cursor()
        cursor.execute(f'UPDATE "CompanionApp_user" set gpa = {gpa} where id={user_id}')
        
        return JsonResponse({'list': 'se matriculo al estudiante'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getUserId(request):
    if request.method == 'GET':
        authorization = request.META.get('HTTP_AUTHORIZATION')
        authorization = authorization.split()
        token = authorization[1]
        cursor = connection.cursor()
        cursor.execute(f'SELECT user_id from "authtoken_token" where key = \'{token}\'')
        user_id = cursor.fetchone()
        user_id = user_id[0]
        return JsonResponse({'user_id': user_id}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getFacultyUser(request):
    if request.method == 'GET':
        print(request.query_params)
        user_id = request.query_params['id']
        user_id = int(user_id)
        cursor = connection.cursor()
        cursor.execute(f'select fname from "CompanionApp_facultad" where id in (select fac_id_id from "CompanionApp_user" where id={user_id})')
        facultyName = cursor.fetchone()
        return JsonResponse({'FacultyName': facultyName}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getAllCoursesUserHasTaken(request):
    if request.method == 'GET':
        user_id = int(request.query_params['user_id'])
        cursor = connection.cursor()
        cursor.execute(f'SELECT c.name, c.code, c.creditos, m.user_id_id, m.year, m.semestre, m.grade FROM "CompanionApp_curso" c INNER JOIN "CompanionApp_matricula" m ON (c.id = m.course_id_id) where m.user_id_id = {user_id} and m.grade <> \'N%\' order by m.year ASC, m.semestre ASC')
        fetchCourses = cursor.fetchall()
        courses = []
        # convert courses to an array of objects
        for i in range(0, len(fetchCourses)):
            dic = {'name': fetchCourses[i][0], 'code': fetchCourses[i][1], 'creditos': fetchCourses[i][2], 'year': fetchCourses[i][4], 'semestre': fetchCourses[i][5], 'grade': fetchCourses[i][6]}
            courses.append(dic)

        return JsonResponse({'list': courses}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAllCoursesBySemester(request):
    if request.method == 'GET': 
        user_id = int(request.query_params['user_id'])
        year = int(request.query_params['year'])
        semestre = int(request.query_params['semestre'])
        cursor = connection.cursor()
        cursor.execute(f'SELECT c.name, c.code, c.creditos, m.user_id_id, m.year, m.semestre, m.grade FROM "CompanionApp_curso" c INNER JOIN "CompanionApp_matricula" m ON (c.id = m.course_id_id) where m.user_id_id = {user_id} and m.year = {year} and m.semestre = {semestre} and m.grade <> \'N%\' ')
        fetchCourses = cursor.fetchall()
        courses = []

        # convert courses to an array of objects
        for i in range(0, len(fetchCourses)):
            dic = {'name': fetchCourses[i][0], 'code': fetchCourses[i][1], 'creditos': fetchCourses[i][2], 'year': fetchCourses[i][4], 'semestre': fetchCourses[i][5], 'grade': fetchCourses[i][6]}
            courses.append(dic)
            
        return JsonResponse({'list': courses}, status=status.HTTP_200_OK)


@api_view(['POST',])
def seeGPA(request):
    if request.method == 'POST':
        user_id = int(request.data['user_id'])
        cursor = connection.cursor()
        cursor.execute(f'SELECT gpa from "CompanionApp_user" where id={user_id}')
        GPA = cursor.fetchone()
        return JsonResponse({'gpa': GPA}, status = status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def hello_world(request):
    # if request.user.is_authenticated:
    if request.method == 'GET':
        return JsonResponse({'msg': request.user.email}, status = status.HTTP_200_OK)
    return JsonResponse({'msg': 'no'})


# delete course and update credits_taken