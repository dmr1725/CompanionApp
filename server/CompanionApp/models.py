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

class User(AbstractUser):
    gpa = models.DecimalField(default = 0, max_digits = 3, decimal_places = 2)
    fac_id = models.ForeignKey(Facultad, on_delete=models.CASCADE, default=1)
    credits_taken = models.IntegerField(default=0)
    credits_taken_score = models.IntegerField(default=0)
    current_year = models.IntegerField(default=1)
    current_semester = models.IntegerField(default=1)

class Matricula(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    course_id = models.ForeignKey(Curso, on_delete=models.CASCADE, default=1)
    section = models.CharField(max_length=5, null=True, blank=True)
    prof = models.CharField(max_length=150, null=True, blank=True)
    semestre = models.IntegerField(default=0, null=False, blank=False)
    year = models.IntegerField(default=0, null=False, blank=False)
    # fecha = models.CharField(max_length=150, null=False, blank=True)
    grade = models.CharField(max_length=3, default = 'N')
    salones =models.CharField(max_length=100,blank=True, null=True) 
    horarios =models.CharField(max_length=150,blank=True, null=True) 
    dias =models.CharField(max_length=100,blank=True, null=True) 


class ProximoSemestre(models.Model):
    course_id = models.ForeignKey(Curso, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=15)
    creditos = models.IntegerField(default=0)
    section = models.CharField(max_length=5, null=True, blank=True)
    prof = models.CharField(max_length=150, null=True, blank=True)
    hours =models.CharField(max_length=150,blank=True, null=True) 
    days =models.CharField(max_length=100,blank=True, null=True) 
    rooms =models.CharField(max_length=100,blank=True, null=True) 