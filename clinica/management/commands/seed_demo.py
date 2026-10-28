"""
============================================================================
Comando de gestión: seed_demo
----------------------------------------------------------------------------
Archivo: clinica/management/commands/seed_demo.py
Propósito:
    Poblar la base de datos con datos realistas para demostrar el sistema
    durante la defensa de la EVA 3. Crea tutores, mascotas, profesionales,
    disponibilidades y citas.
============================================================================
"""

from datetime import time, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from clinica.models import Tutor, Mascota, Profesional, Disponibilidad, Cita

class Command(BaseCommand):
    help = 'Carga datos demo para la defensa'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos demo...')

        # Limpiar datos previos (opcional, cuidado en producción)
        # Cita.objects.all().delete()
        # Mascota.objects.all().delete()
        # Tutor.objects.all().delete()
        # Profesional.objects.all().delete()

        # 1. Profesionales
        vet1, _ = Profesional.objects.get_or_create(
            email='cperez@petcare.cl',
            defaults={'nombre': 'Carlos Pérez', 'especialidad': 'Medicina General'}
        )
        vet2, _ = Profesional.objects.get_or_create(
            email='mlopez@petcare.cl',
            defaults={'nombre': 'María López', 'especialidad': 'Cirugía'}
        )

        for vet in [vet1, vet2]:
            for dia in ['LUN', 'MAR', 'MIE', 'JUE', 'VIE']:
                Disponibilidad.objects.get_or_create(
                    profesional=vet,
                    dia_semana=dia,
                    hora_inicio=time(9, 0),
                    hora_fin=time(18, 0)
                )

        # 2. Tutores y Mascotas
        t1, _ = Tutor.objects.get_or_create(
            rut='11111111-1',
            defaults={'nombre': 'Ana Silva', 'email': 'ana@example.cl', 'telefono': '+56911111111'}
        )
        m1, _ = Mascota.objects.get_or_create(
            nombre='Firulais', tutor=t1,
            defaults={'especie': Mascota.ESPECIE_PERRO, 'raza': 'Quiltro', 'fecha_nacimiento': '2021-03-15'}
        )

        t2, _ = Tutor.objects.get_or_create(
            rut='22222222-2',
            defaults={'nombre': 'Pedro Soto', 'email': 'pedro@example.cl', 'telefono': '+56922222222'}
        )
        m2, _ = Mascota.objects.get_or_create(
            nombre='Michi', tutor=t2,
            defaults={'especie': Mascota.ESPECIE_GATO, 'raza': 'Siames', 'fecha_nacimiento': '2022-06-10'}
        )

        # 3. Citas (buscar el próximo lunes para evitar errores de fecha)
        hoy = timezone.now()
        dias_hasta_lunes = (0 - hoy.weekday()) % 7 or 7
        proximo_lunes = (hoy + timedelta(days=dias_hasta_lunes)).replace(hour=10, minute=0, second=0, microsecond=0)

        # Cita válida 1
        Cita.objects.get_or_create(
            mascota=m1, profesional=vet1, fecha_hora=proximo_lunes,
            defaults={'duracion_min': 30, 'motivo': 'Control anual', 'estado': Cita.ESTADO_CONFIRMADA}
        )

        # Cita válida 2 (más tarde el mismo día)
        Cita.objects.get_or_create(
            mascota=m2, profesional=vet2, fecha_hora=proximo_lunes.replace(hour=11, minute=30),
            defaults={'duracion_min': 45, 'motivo': 'Vacunación', 'estado': Cita.ESTADO_PENDIENTE}
        )

        self.stdout.write(self.style.SUCCESS('✔ Datos demo cargados correctamente.'))