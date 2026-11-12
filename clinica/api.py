from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Profesional, Mascota, Cita, Tutor
from .serializers import ProfesionalSerializer, MascotaSerializer, CitaSerializer, TutorSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def lista_profesionales(request):
    profesionales = Profesional.objects.filter(activo=True)
    return Response(ProfesionalSerializer(profesionales, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def lista_mascotas(request):
    mascotas = Mascota.objects.all()
    return Response(MascotaSerializer(mascotas, many=True).data)

@api_view(['POST'])
@permission_classes([AllowAny])
def crear_cita(request):
    serializer = CitaSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_tutor_mascota(request):
    try:
        data = request.data
        tutor = TutorSerializer(data={
            'nombre': data.get('tutor_nombre'),
            'rut': data.get('tutor_rut', f"TEMP-{data.get('tutor_telefono')}"),
            'email': data.get('tutor_email', ''),
            'telefono': data.get('tutor_telefono')
        })
        if not tutor.is_valid():
            return Response({"error": "Datos del tutor inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        t = tutor.save()

        mascota = MascotaSerializer(data={
            'nombre': data.get('mascota_nombre'),
            'especie': data.get('mascota_especie', 'PERRO'),
            'fecha_nacimiento': '2020-01-01',
            'tutor': t.id
        })
        if not mascota.is_valid():
            t.delete()
            return Response({"error": "Datos de la mascota inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        m = mascota.save()

        return Response({"mascota_id": m.id, "mascota_nombre": m.nombre}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)