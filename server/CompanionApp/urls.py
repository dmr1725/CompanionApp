# from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf.urls import url, include 


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/insertar_fac$', views.insertarFacultades),
    url(r'^api/hello$', views.hello_world),
    url(r'^api/insertar_cursos$', views.insertarTodosLosCursos),
    url(r'^api/update_faculty$', views.updateFaculty),
    url(r'^api/find_course$', views.findCourse),
    url(r'^api/add_taken_course$', views.addTakenCourse)

]

