"""
============================================================================
Seed de datos demo — Fase 1 PetCare EVA3
----------------------------------------------------------------------------
Ejecutar con:
    python manage.py shell -c "exec(open('scripts/seed_fase1.py', encoding='utf-8').read())"

Propósito:
    Carga 1 tutor, 1 mascota, 1 profesional, 5 disponibilidades, 1 cita
    válida, 1 ficha clínica y 1 recordatorio. Idempotente.
============================================================================
"""
from datetime import time, timedelta
from django.utils import timezone
from clinica.models import (
    Cita, Disponibilidad, FichaClinica, Mascota,
    Profesional, Recordatorio, Tutor,
)

# 1) Limpieza
Recordatorio.objects.all().delete()
FichaClinica.objects.all().delete()
Cita.objects.all().delete()
Disponibilidad.objects.all().delete()
Mascota.objects.all().delete()
Profesional.objects.all().delete()
Tutor.objects.all().delete()
print("[1/6] BD limpiada.")

# 2) Tutor
tutor = Tutor.objects.create(
    nombre="María González",
    rut="12345678-9",
    email="maria@example.cl",
    telefono="+56911112222",
    direccion="Av. Siempre Viva 742",
)
print("[2/6] Tutor:", tutor)

# 3) Mascota
mascota = Mascota.objects.create(
    nombre="Rocky",
    especie=Mascota.ESPECIE_PERRO,
    raza="Labrador",
    fecha_nacimiento="2020-05-10",
    tutor=tutor,
)
print("[3/6] Mascota:", mascota)

# 4) Profesional + disponibilidad L-V 09:00-18:00
vet = Profesional.objects.create(
    nombre="Carlos Pérez",
    especialidad="Medicina General",
    email="cperez@petcare.cl",
)
for dia in ["LUN", "MAR", "MIE", "JUE", "VIE"]:
    Disponibilidad.objects.create(
        profesional=vet,
        dia_semana=dia,
        hora_inicio=time(9, 0),
        hora_fin=time(18, 0),
    )
print("[4/6] Profesional:", vet, "| Disponibilidades:", vet.disponibilidades.count())

# 5) Cita válida (próximo lunes 10:00) + Ficha clínica
hoy = timezone.now()
dias_hasta_lunes = (0 - hoy.weekday()) % 7 or 7
proximo_lunes = (hoy + timedelta(days=dias_hasta_lunes)).replace(
    hour=10, minute=0, second=0, microsecond=0,
)
cita = Cita(
    mascota=mascota,
    profesional=vet,
    fecha_hora=proximo_lunes,
    duracion_min=30,
    motivo="Vacunación anual",
)
cita.full_clean()
cita.save()
print("[5/6] Cita:", cita)

ficha = FichaClinica.objects.create(
    cita=cita,
    diagnostico="Paciente sano, vacunas al día.",
    tratamiento="Aplicación de vacuna antirrábica.",
)
print("      Ficha:", ficha)

# 6) Recordatorio de control a 180 días
recordatorio = Recordatorio.objects.create(
    mascota=mascota,
    tipo=Recordatorio.TIPO_CONTROL,
    fecha_programada=(timezone.now() + timedelta(days=180)).date(),
    notas="Control semestral post-vacunación.",
)
print("[6/6] Recordatorio:", recordatorio)

# Resumen
print("\n=== RESUMEN FINAL ===")
print("Tutores:", Tutor.objects.count())
print("Mascotas:", Mascota.objects.count())
print("Profesionales:", Profesional.objects.count())
print("Disponibilidades:", Disponibilidad.objects.count())
print("Citas:", Cita.objects.count())
print("Fichas:", FichaClinica.objects.count())
print("Recordatorios:", Recordatorio.objects.count())