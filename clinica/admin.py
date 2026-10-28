"""
============================================================================
Registro básico en Django Admin — PetCare EVA3
----------------------------------------------------------------------------
Archivo: clinica/admin.py
Propósito:
    Registra los 7 modelos del dominio en el Django Admin para que sean
    visibles en /admin/. Esta es la versión BÁSICA de la Fase 1: solo
    registra los modelos para poder probar. La personalización completa
    (filtros, búsquedas, inlines, template custom) se hará en Fase 2.
============================================================================
"""

from django.contrib import admin

from .models import (
    Cita,
    Disponibilidad,
    FichaClinica,
    Mascota,
    Profesional,
    Recordatorio,
    Tutor,
)


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Registro básico de Tutores."""

    list_display = ('nombre', 'rut', 'email', 'telefono')


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    """Registro básico de Mascotas."""

    list_display = ('nombre', 'especie', 'raza', 'tutor')


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    """Registro básico de Profesionales."""

    list_display = ('nombre', 'especialidad', 'email', 'activo')


@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    """Registro básico de Disponibilidades."""

    list_display = ('profesional', 'dia_semana', 'hora_inicio', 'hora_fin')


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    """Registro básico de Citas."""

    list_display = ('mascota', 'profesional', 'fecha_hora', 'duracion_min', 'estado')


@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    """Registro básico de Fichas Clínicas."""

    list_display = ('cita', 'fecha_creacion')


@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    """Registro básico de Recordatorios."""

    list_display = ('mascota', 'tipo', 'fecha_programada', 'enviado')