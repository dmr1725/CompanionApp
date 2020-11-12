from .models import Facultad, Curso, Matricula
from rest_framework import serializers

class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = ('__all__')
    
    def create(self, validated_data):
        instance, created = Facultad.objects.get_or_create(**validated_data)
        # print(instance, created)
        if(created == False):
            print('ya se creo')
        return validated_data

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ('__all__')
    

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ('__all__')
    
    def create(self, validated_data):
        instance, created = Matricula.objects.get_or_create(**validated_data)
        # print(instance, created)
        if(created == False):
            print('ya se creo')
        return validated_data

