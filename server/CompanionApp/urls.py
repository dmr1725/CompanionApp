# from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url, include 
from django.urls import path


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/insertar_fac$', views.insertarFacultades),
    url(r'^api/hello$', views.hello_world),
    url(r'^api/insertar_cursos$', views.insertarTodosLosCursos),
    url(r'^api/update_faculty$', views.updateFaculty),
    url('api/find_course', views.findCourse),
    url('api/select_course_prox_semestre', views.selectCourseProxSemestre),
    url(r'^api/add_taken_course$', views.addTakenCourse),
    url(r'^api/get_user_id$', views.getUserId),
    url('api/get_faculty_name', views.getFacultyUser),
    url('api/get_all_courses_user_has_taken', views.getAllCoursesUserHasTaken),
    url('api/get_all_courses_by_semester', views.getAllCoursesBySemester),
    url('api/see_gpa', views.seeGPA),
    url('api/insertar_prox_sem_cursos', views.insertarTodosLosCursosProxSemestre),
    url('api/matricular_prox_semestre', views.matricularProxSemestre),
    url('api/get_current_courses', views.getMyCurrentCourses),
    url('api/update_grade_and_gpa', views.updateGradeAndGPA),
    url('api/delete_course', views.deleteCourse),
    url('api/get_year_and_semester', views.getSemesterAndYear),
    url('api/update_year_and_semester', views.updateSemesterAndYear),

]

