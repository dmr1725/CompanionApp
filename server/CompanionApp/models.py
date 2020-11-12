from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# diego, Diego1999$

class Facultad(models.Model):
    fname = models.CharField(max_length=150)

class Curso(models.Model):
    fac_id = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=9)
    creditos = models.IntegerField(default=0)

class Matricula(models.Model):
    course_id = models.ForeignKey(Curso, on_delete=models.CASCADE)
    section = models.CharField(max_length=5)
    prof = models.CharField(max_length=150)
    grade = models.CharField(max_length=3, default = 'N')
    semestre = models.IntegerField(default=0)

class User(AbstractUser):
    gpa = models.DecimalField(default = 0, max_digits = 3, decimal_places = 2)
    fac_id = models.ForeignKey(Facultad, on_delete=models.CASCADE, default=1)
