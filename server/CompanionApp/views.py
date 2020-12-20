import sys
import json
sys.path.insert(1,'C:/Users/diego/Documents/companion_app_gh/organizar/')


from organizar import files3, proxSemFiles


from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.account.views import LogoutView


from django.db import connection

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import Facultad, Curso, ProximoSemestre
from .serializers import FacultadSerializer, CursoSerializer
from rest_framework.decorators import api_view




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
                        elif 'LAB' in key and (name != 'LABORATORIO' or name != 'LABORATORIO ' or name != 'TALLER' or name != 'TALLER ' or name != 'CONFERENCIA' or name != 'CONFERENCIA '):
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
                        print('hola')
                        # create course
                        cursor = connection.cursor()
                        cursor.execute(f'INSERT INTO "CompanionApp_curso" (name, code, creditos, fac_id_id) VALUES (\'{name}\', \'{code}\', {creditos}, {fac_id})')
                        
                         # once created the course, fetch the course_id
                        cursor = connection.cursor()
                        cursor.execute(f'SELECT id from "CompanionApp_curso" where code = \'{code}\'')
                        course_id = cursor.fetchone()
                    
                    # getting course_id from line 128 or 116
                    course_id = course_id[0]

                    # before inserting course, check if that course with section is already in the table ProximoSemestre
                    cursor = connection.cursor()
                    cursor.execute(f'Select id from "CompanionApp_proximosemestre" where code=\'{code}\' and section=\'{section}\'')
                    prox_sem_id = cursor.fetchone() # id from table 
    
                    # if course with section does not exist, insert it in the table ProximoSemestre
                    if prox_sem_id == None:
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
            return JsonResponse({'msg': 'Insert A, B, C, D or F' }, status=status.HTTP_200_OK)

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
                return JsonResponse({'msg': 'You already took the course that year and semester.' }, status=status.HTTP_200_OK)
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
        print('ya')
        
        return JsonResponse({'msg': 'Ok, you can see that course in your curriculum'}, status=status.HTTP_201_CREATED)


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
        cursor.execute(f'SELECT c.name, c.code, c.creditos, m.user_id_id, m.year, m.semestre, m.grade, c.id FROM "CompanionApp_curso" c INNER JOIN "CompanionApp_matricula" m ON (c.id = m.course_id_id) where m.user_id_id = {user_id} and m.grade <> \'N%\' order by m.year ASC, m.semestre ASC')
        fetchCourses = cursor.fetchall()
        courses = []
        # convert courses to an array of objects
        for i in range(0, len(fetchCourses)):
            dic = {'name': fetchCourses[i][0], 'code': fetchCourses[i][1], 'creditos': fetchCourses[i][2], 'year': fetchCourses[i][4], 'semestre': fetchCourses[i][5], 'grade': fetchCourses[i][6], 'course_id': fetchCourses[i][7]}
            courses.append(dic)

        return JsonResponse({'list': courses}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAllCoursesBySemester(request):
    if request.method == 'GET': 
        user_id = int(request.query_params['user_id'])
        year = int(request.query_params['year'])
        semestre = int(request.query_params['semestre'])
        cursor = connection.cursor()
        cursor.execute(f'SELECT c.name, c.code, c.creditos, m.user_id_id, m.year, m.semestre, m.grade, c.id FROM "CompanionApp_curso" c INNER JOIN "CompanionApp_matricula" m ON (c.id = m.course_id_id) where m.user_id_id = {user_id} and m.year = {year} and m.semestre = {semestre} and m.grade <> \'N%\' ')
        fetchCourses = cursor.fetchall()
        courses = []

        # convert courses to an array of objects
        for i in range(0, len(fetchCourses)):
            dic = {'name': fetchCourses[i][0], 'code': fetchCourses[i][1], 'creditos': fetchCourses[i][2], 'year': fetchCourses[i][4], 'semestre': fetchCourses[i][5], 'grade': fetchCourses[i][6], 'course_id': fetchCourses[i][7]}
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

@api_view(['POST',])
def matricularProxSemestre(request):
    if request.method == 'POST':
        # data from request
        user_id = int(request.data['user_id'])
        isSummer = request.data['isSummer']
        course_id = int(request.data['course_id'])


        # selecting current year and current semester of user from database
        cursor = connection.cursor()
        cursor.execute(f'Select current_year, current_semester from "CompanionApp_user" where id = {user_id} ')
        info = cursor.fetchone()
        current_year = info[0]
        current_semester = info[1]

        # determining next semester and next year
        if (current_semester == 2 and isSummer == 'false') or current_semester == 3:
            next_semester = 1
            next_year = current_year + 1
        elif (current_semester == 2 and isSummer == 'true'):
            next_semester = current_semester + 1 # 3
            next_year = current_year # stays the same
        elif current_semester == 1:
            next_semester = current_semester + 1 # 2
            next_year = current_year

        # selecting all attributes of course from course_id
        cursor = connection.cursor()
        cursor.execute(f'Select * from "CompanionApp_proximosemestre" where id = {course_id} ')
        info = cursor.fetchone() 
        course_name = info[1]
        course_code = info[2]
        course_section = info[4]
        course_prof = info[5]
        course_hours = info[6]
        course_days = info[7]
        course_rooms = info[8]
        course_id = info[9] # course_id in "CompanionApp_curso"
        course_grade = 'N' # N de none, por ahora no hay nota
        
        # see if student already enrolled for the class
        cursor = connection.cursor()
        cursor.execute(f'Select id from "CompanionApp_matricula" where course_id_id={course_id} and section=\'{course_section}\' and prof=\'{course_prof}\' and horarios=\'{course_hours}\' and dias=\'{course_days}\' and salones=\'{course_rooms}\' and semestre={next_semester} and year={next_year} and user_id_id={user_id}')
        info = cursor.fetchone() 
        print(info)
        if info != None:
            return JsonResponse({'msg': 'Ya estabas matriculado'}, status=status.HTTP_201_CREATED)
        else:
            # enroll student
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO "CompanionApp_matricula" (section, prof, semestre, year, grade, salones, horarios, dias, course_id_id, user_id_id) VALUES (\'{course_section}\',\'{course_prof}\', {next_semester}, {next_year}, \'{course_grade}\', \'{course_rooms}\', \'{course_hours}\', \'{course_days}\', {course_id}, {user_id})')

        return JsonResponse({'msg': 'te matriculaste a ' + course_code + '-' + course_section}, status=status.HTTP_201_CREATED)


@api_view(['POST',])
def getMyCurrentCourses(request):
    if request.method == 'POST':
        user_id = int(request.data['user_id'])
        current_courses = [] 

        # find current year of student
        cursor = connection.cursor()
        cursor.execute(f'select max(year) from "CompanionApp_matricula" where user_id_id={user_id}')
        current_year = cursor.fetchone()

        if current_year[0] == None:
            return JsonResponse({'msg': 'No tienes cursos'}, status = status.HTTP_200_OK)

        else:
            current_year = int(current_year[0])


        # find current semester of student, based on the current_year
        cursor = connection.cursor()
        cursor.execute(f'select max(semestre) from "CompanionApp_matricula" where year = {current_year} and user_id_id = {user_id}')
        current_semester = cursor.fetchone()
        current_semester = int(current_semester[0])

        # find current courses based on current_semester and current_year
        cursor = connection.cursor()
        cursor.execute(f'select c.id, c.name, c.code, m.year, m.semestre, m.section, m.prof, m.salones, m.horarios, m.dias from "CompanionApp_matricula" m INNER JOIN "CompanionApp_curso" c on c.id = m.course_id_id where m.year = {current_year} and m.semestre={current_semester} and m.user_id_id={user_id}')
        fetchCourses = cursor.fetchall()

        # convert courses array into dictionary
        for i in range(0, len(fetchCourses)):
            # if fetchCourses[i][2] == None, this means that the rest of the array will also be none. 
            # The reason for this is that when users AddTakenCourses, they just add the course code
            if fetchCourses[i][5] == None:
                dic = {'id': fetchCourses[i][0], 'name': fetchCourses[i][1], 'code': fetchCourses[i][2], 'year': fetchCourses[i][3], 'semestre': fetchCourses[i][4]}
            
            # here we have all the elements because users enrolled from the courses in table ProximoSemestre
            else:    
                dic = {'id': fetchCourses[i][0], 'name': fetchCourses[i][1], 'code': fetchCourses[i][2], 'year': fetchCourses[i][3], 'semestre': fetchCourses[i][4], 'section': fetchCourses[i][5], 'prof': fetchCourses[i][6], 'salones': fetchCourses[i][7], 'horarios': fetchCourses[i][8], 'dias': fetchCourses[i][9]}

            current_courses.append(dic)


       

    return JsonResponse({'list': current_courses}, status = status.HTTP_200_OK)

@api_view(['PATCH',])
def updateGradeAndGPA(request):
    if request.method == 'PATCH':
        new_grade = request.data['grade']
        course_id = int(request.data['course_id'])
        year = int(request.data['year'])
        semestre = int(request.data['semestre'])
        user_id = int(request.data['user_id'])
        current_points = 0 # to deal with current_grade
        new_points = 0 # to deal with new_grade

        # points of new_grade
        if new_grade == 'A':
            new_points = 4
        elif new_grade == 'B':
            new_points = 3
        elif new_grade == 'C':
            new_points = 2
        elif new_grade == 'D':
            new_points = 1
        elif new_grade == 'F':
            new_points = 0

        # get credits from the course
        cursor = connection.cursor()
        cursor.execute(f'select creditos from "CompanionApp_curso" where id={course_id}')
        creditos = cursor.fetchone()
        creditos = creditos[0]
        
        # select current grade
        cursor = connection.cursor()
        cursor.execute(f'select grade from "CompanionApp_matricula" where course_id_id={course_id} and user_id_id={user_id} and year={year} and semestre={semestre}')
        current_grade = cursor.fetchone()
        current_grade = current_grade[0]
        print(current_grade)

        # this means that the credits for this course had not been added to the column credits_taken from table "CompanionApp_curso"
        if current_grade == 'N':
            # get credits_taken. Then add the courses credits to credits_taken
            cursor = connection.cursor()
            cursor.execute(f'select credits_taken from "CompanionApp_user" where id={user_id}')
            credits_taken = cursor.fetchone()
            credits_taken = credits_taken[0]
            new_credits_taken = credits_taken + creditos
            print(new_credits_taken, 'New credits taken')

            # get credits_taken_score. Then multiply credits * new_points and add it to credits_taken_score
            cursor = connection.cursor()
            cursor.execute(f'select credits_taken_score from "CompanionApp_user" where id={user_id}')
            credits_taken_score = cursor.fetchone()
            credits_taken_score = credits_taken_score[0]
            new_credits_taken_score = credits_taken_score + (new_points * creditos)
            print(new_credits_taken_score, 'New credits taken score')

            # update gpa, credits_taken, credits_taken_score
            gpa = (new_credits_taken_score / new_credits_taken)
            gpa = float("{:.2f}".format(gpa))
            print(gpa, 'new gpa')
            cursor = connection.cursor()
            cursor.execute(f'UPDATE "CompanionApp_user" set gpa = {gpa}, credits_taken = {new_credits_taken}, credits_taken_score={new_credits_taken_score} where id={user_id}')

            # update grade in table CompanionApp_matricula
            cursor = connection.cursor()
            cursor.execute(f'UPDATE "CompanionApp_matricula" set grade=\'{new_grade}\' where user_id_id={user_id} and semestre={semestre} and year={year} and course_id_id={course_id} ')
            return JsonResponse({'msg': 'Your GPA was updated to ' + str(gpa)}, status = status.HTTP_202_ACCEPTED)

        # else student already has a grade and wants to replace it
        else:
            if current_grade == 'A':
                current_points = 4
            elif current_grade == 'B':
                current_points = 3
            elif current_grade == 'C':
                current_points = 2
            elif current_grade == 'D':
                current_points = 1
            elif current_grade == 'F':
                current_points = 0
            
            # get credits_taken_score and credits_taken. Then substract (creditos * current_points) to credits_taken_score. Then add (creditos * new_points) to credits_taken_score
            cursor = connection.cursor()
            cursor.execute(f'select credits_taken_score, credits_taken from "CompanionApp_user" where id={user_id}')
            results = cursor.fetchone()
            credits_taken_score = results[0]
            credits_taken = results[1]
            new_credits_taken_score = credits_taken_score - (creditos * current_points)
            new_credits_taken_score = new_credits_taken_score + (creditos * new_points)
            print(new_credits_taken_score, 'new credits taken score')
            print(credits_taken, 'credits taken')

            # update gpa and credits_taken_score. credits_taken stays the same
            gpa = (new_credits_taken_score / credits_taken)
            gpa = float("{:.2f}".format(gpa))
            print(gpa, 'new gpa')
            cursor = connection.cursor()
            cursor.execute(f'UPDATE "CompanionApp_user" set gpa = {gpa}, credits_taken_score={new_credits_taken_score} where id={user_id}')

             # update grade in table CompanionApp_matricula
            cursor = connection.cursor()
            cursor.execute(f'UPDATE "CompanionApp_matricula" set grade=\'{new_grade}\' where user_id_id={user_id} and semestre={semestre} and year={year} and course_id_id={course_id} ')
            return JsonResponse({'msg': 'Your GPA was updated to ' + str(gpa)}, status = status.HTTP_202_ACCEPTED)

@api_view(['DELETE',])
def deleteCourse(request):
    if request.method == 'DELETE':
        course_id = int(request.data['course_id'])
        year = int(request.data['year'])
        semestre = int(request.data['semestre'])
        user_id = int(request.data['user_id'])

        # get credits from the course
        cursor = connection.cursor()
        cursor.execute(f'select creditos from "CompanionApp_curso" where id={course_id}')
        creditos = cursor.fetchone()
        creditos = creditos[0]
        print(creditos)
        
        # select current grade
        cursor = connection.cursor()
        cursor.execute(f'select grade from "CompanionApp_matricula" where course_id_id={course_id} and user_id_id={user_id} and year={year} and semestre={semestre}')
        current_grade = cursor.fetchone()
        current_grade = current_grade[0]
        print(current_grade)

        if current_grade == 'N':
            # just delete course from table CompanionApp_matricula
            cursor = connection.cursor()
            cursor.execute(f'DELETE from "CompanionApp_matricula" where user_id_id={user_id} and course_id_id = {course_id} and year={year} and semestre={semestre}')
            return JsonResponse({'msg': 'SUCCESS' }, status = status.HTTP_202_ACCEPTED)
        
        else:
            # update credits_taken, credits_taken_score and gpa
            current_points = 0
            if current_grade == 'A':
                current_points = 4
            elif current_grade == 'B':
                current_points = 3
            elif current_grade == 'C':
                current_points = 2
            elif current_grade == 'D':
                current_points = 1
            elif current_grade == 'F':
                current_points = 0
            
            # get credits_taken_score and credits_taken. Then, substract (creditos * current_points) to credits_taken_score and substract creditos to credits_taken
            cursor = connection.cursor()
            cursor.execute(f'select credits_taken_score, credits_taken from "CompanionApp_user" where id={user_id}')
            results = cursor.fetchone()
            credits_taken_score = results[0]
            credits_taken = results[1]

            new_credits_taken_score = credits_taken_score - (current_points * creditos)
            new_credits_taken = credits_taken - creditos
            if new_credits_taken == 0:
                gpa = 0.00
            else:
                gpa = new_credits_taken_score / new_credits_taken 
                gpa = float("{:.2f}".format(gpa))
            print(new_credits_taken, 'credits taken')
            print(new_credits_taken_score, 'credits taken score')

            # update gpa, credits_taken and credits_taken_score
            cursor = connection.cursor()
            cursor.execute(f'UPDATE "CompanionApp_user" set gpa = {gpa}, credits_taken = {new_credits_taken}, credits_taken_score={new_credits_taken_score} where id={user_id}')

            # delete course from "CompanionApp_matricula"
            cursor = connection.cursor()
            cursor.execute(f'DELETE from "CompanionApp_matricula" where user_id_id={user_id} and course_id_id = {course_id} and year={year} and semestre={semestre}')


            return JsonResponse({'msg': 'SUCCESS' }, status = status.HTTP_202_ACCEPTED)

@api_view(['PATCH',])
def updateSemesterAndYear(request):
    if request.method == 'PATCH':
        user_id = int(request.data['user_id'])
        year = int(request.data['year'])
        semestre = int(request.data['semester'])

        # update semestre and year for user. This is for knowing which year and semester he/she is currently in
        cursor = connection.cursor()
        cursor.execute(f'UPDATE "CompanionApp_user" set current_year={year}, current_semester={semestre} where id={user_id}')
        return JsonResponse({'msg': 'SUCCESS' }, status = status.HTTP_202_ACCEPTED)
        

@api_view(['POST',])
def getSemesterAndYear(request):
    if request.method == 'POST':
        user_id = int(request.data['user_id'])

        cursor = connection.cursor()
        cursor.execute(f'select current_year, current_semester from "CompanionApp_user" where id={user_id}')
        info = cursor.fetchone()
        year = info[0]
        semestre = info[1]
        return JsonResponse({'msg': {'year': year, 'semestre': semestre} }, status = status.HTTP_202_ACCEPTED)
        

@api_view(['POST',])
def logout(request):
    request.user.auth_token.delete()
    return JsonResponse({"success": "Successfully logged out."}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def hello_world(request):
    # if request.user.is_authenticated:
    if request.method == 'GET':
        return JsonResponse({'msg': request.user.email}, status = status.HTTP_200_OK)
    return JsonResponse({'msg': 'no'})


# delete course and update credits_takenv