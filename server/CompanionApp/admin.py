from django.contrib import admin
from .models import Curso, Facultad, User,Matricula, ProximoSemestre

# Register your models here.
admin.site.register(Facultad)
admin.site.register(Curso)
admin.site.register(User)
admin.site.register(Matricula)
admin.site.register(ProximoSemestre)
