from rest_framework import serializers
from .models import Tutor, Mascota, Profesional, Cita

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'nombre', 'rut', 'email', 'telefono']

class MascotaSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.ReadOnlyField(source='tutor.nombre')
    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'especie', 'raza', 'sexo', 'tutor', 'tutor_nombre']

class ProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesional
        fields = ['id', 'nombre', 'especialidad']

class CitaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.ReadOnlyField(source='mascota.nombre')
    profesional_nombre = serializers.ReadOnlyField(source='profesional.nombre')
    class Meta:
        model = Cita
        fields = ['id', 'mascota', 'mascota_nombre', 'profesional', 'profesional_nombre', 'fecha_hora', 'duracion_min', 'motivo', 'estado']