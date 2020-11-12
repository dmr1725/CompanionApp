from django.contrib import admin
from .models import Curso, Matricula, Facultad, User

# Register your models here.
admin.site.register(Curso)
admin.site.register(Matricula)
admin.site.register(Facultad)
admin.site.register(User)
