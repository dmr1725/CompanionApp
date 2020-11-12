import sys
import json
sys.path.insert(1,'C:/Users/diego/Documents/companion_app3/organizar/')

from organizar import files3


from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import Facultad, Curso
from .serializers import FacultadSerializer, CursoSerializer, MatriculaSerializer
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
            path = "C:/Users/diego/Documents/companion_app3/segundo_sem" if check[0][-1] == '2' else "C:/Users/diego/Documents/companion_app3/primer_sem"
            with open(path + '/' + file['file']) as f:
                data = json.load(f)
                fac_id = file['num']
                for key in data:
                    if key != 'Horario ':
                        code = key
                        name = data[key][0]
                        creds = data[key][1]
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
def matricula(request):
    if request.method == 'POST':
        matricula_serializer = MatriculaSerializer(data = {'course_id': request.data['course_id_id'], 'section': request.data['section'], 'prof': request.data['prof'], 'semestre': request.data['semestre']})
        if matricula_serializer.is_valid():
            matricula_serializer.save()
            return JsonResponse({'message': 'se inserto matricula'})
        return JsonResponse({'message': 'error'})




@api_view(['GET', 'POST'])
def hello_world(request):
    # if request.user.is_authenticated:
    if request.method == 'GET':
        return JsonResponse({'msg': request.user.email}, status = status.HTTP_200_OK)
    return JsonResponse({'msg': 'no'})


