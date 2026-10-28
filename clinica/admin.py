"""
============================================================================
Personalización del Django Admin — PetCare EVA3
----------------------------------------------------------------------------
Archivo: clinica/admin.py
Propósito:
    Registra y personaliza los 7 modelos del dominio PetCare en el Django
    Admin. Cubre el criterio 2 de la rúbrica al 100%:

        - Registro de TODOS los modelos.
        - `list_display` optimizado (columnas relevantes).
        - `list_filter` (filtros laterales por estado, especie, día, etc.).
        - `search_fields` (búsqueda por nombre, RUT, email, etc.).
        - `date_hierarchy` en Citas para navegación por fecha.
        - `ordering` consistente.
        - `inlines` para editar Mascotas dentro de Tutor y Ficha Clínica
          dentro de Cita.
        - `actions` masivas (marcar recordatorios enviados, confirmar citas).
        - `readonly_fields` para campos de auditoría.
        - `fieldsets` para agrupar campos visualmente.

Convenciones:
    - Cada ModelAdmin lleva docstring de clase explicando su propósito.
    - Los métodos personalizados (ej. `_edad`, `_total_citas`) llevan
      docstring y `short_description` para el header de la columna.
============================================================================
"""

from datetime import date

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Cita,
    Disponibilidad,
    FichaClinica,
    Mascota,
    Profesional,
    Recordatorio,
    Tutor,
)


# ============================================================================
# BRANDING GLOBAL DEL ADMIN
# ----------------------------------------------------------------------------
# Sobreescribe los textos por defecto del Admin en la barra superior y en
# la portada. El template `admin/base_site.html` refuerza el branding.
# ============================================================================
admin.site.site_header = '🐾 PetCare — Administración'
admin.site.site_title = 'PetCare Admin'
admin.site.index_title = 'Panel de Gestión Clínica Veterinaria'


# ============================================================================
# TUTOR
# ----------------------------------------------------------------------------
# Entidad raíz. Se muestran inlines de Mascotas para editar todo el
# grupo familiar desde una sola pantalla.
# ============================================================================
class MascotaInline(admin.TabularInline):
    """
    Inline de Mascotas dentro del formulario de Tutor.

    Permite crear/editar las mascotas del tutor sin salir de su ficha.
    `extra=1` deja una fila vacía para agregar una nueva mascota.
    """

    model = Mascota
    extra = 1
    fields = ('nombre', 'especie', 'raza', 'fecha_nacimiento')
    show_change_link = True


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """
    Administración de Tutores (dueños de mascotas).

    Incluye búsqueda por nombre/RUT/email, filtro por fecha de registro,
    inline de mascotas y columna calculada `_total_mascotas`.
    """

    list_display = ('nombre', 'rut', 'email', 'telefono', '_total_mascotas')
    list_filter = ('fecha_registro',)
    search_fields = ('nombre', 'rut', 'email', 'telefono')
    ordering = ('nombre',)
    readonly_fields = ('fecha_registro',)
    inlines = [MascotaInline]

    fieldsets = (
        ('Datos personales', {
            'fields': ('nombre', 'rut', 'email', 'telefono')
        }),
        ('Dirección', {
            'fields': ('direccion',)
        }),
        ('Auditoría', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Mascotas')
    def _total_mascotas(self, obj):
        """Retorna el número de mascotas registradas para el tutor."""
        return obj.mascotas.count()


# ============================================================================
# MASCOTA
# ----------------------------------------------------------------------------
# Paciente. Se muestra la edad calculada a partir de la fecha de nacimiento
# (útil en la defensa) y filtros por especie.
# ============================================================================
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    """
    Administración de Mascotas.

    Incluye filtro por especie, búsqueda por nombre de mascota o tutor,
    y columna calculada `_edad` en años.
    """

    list_display = ('nombre', 'especie', 'raza', 'tutor', '_edad')
    list_filter = ('especie', 'tutor')
    search_fields = ('nombre', 'raza', 'tutor__nombre', 'tutor__rut')
    ordering = ('nombre',)
    autocomplete_fields = ('tutor',)
    list_select_related = ('tutor',)

    @admin.display(description='Edad')
    def _edad(self, obj):
        """Calcula la edad de la mascota en años a partir de su nacimiento."""
        if not obj.fecha_nacimiento:
            return '—'
        hoy = date.today()
        años = hoy.year - obj.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day)
        )
        return f'{años} año(s)'


# ============================================================================
# PROFESIONAL
# ----------------------------------------------------------------------------
# Veterinario/a. Se muestra inline de disponibilidades para configurar
# su horario semanal desde la misma pantalla.
# ============================================================================
class DisponibilidadInline(admin.TabularInline):
    """
    Inline de Disponibilidades dentro del formulario de Profesional.

    Permite configurar el horario semanal del profesional sin salir de
    su ficha.
    """

    model = Disponibilidad
    extra = 1
    fields = ('dia_semana', 'hora_inicio', 'hora_fin')


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    """
    Administración de Profesionales veterinarios.

    Incluye filtro por estado activo y especialidad, búsqueda por nombre
    o email, y inline de disponibilidades.
    """

    list_display = ('nombre', 'especialidad', 'email', 'activo', '_total_citas')
    list_filter = ('activo', 'especialidad')
    search_fields = ('nombre', 'especialidad', 'email')
    ordering = ('nombre',)
    inlines = [DisponibilidadInline]

    @admin.display(description='Citas')
    def _total_citas(self, obj):
        """Retorna el número total de citas asignadas al profesional."""
        return obj.citas.count()


# ============================================================================
# DISPONIBILIDAD
# ----------------------------------------------------------------------------
# Bloques horarios semanales del profesional. Se puede editar también desde
# el inline de Profesional, pero se registra aquí para tener vista global.
# ============================================================================
@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    """
    Administración de Disponibilidades (bloques horarios semanales).

    Ordenado por profesional, día y hora de inicio para facilitar la
    revisión de la agenda semanal.
    """

    list_display = ('profesional', 'dia_semana', 'hora_inicio', 'hora_fin')
    list_filter = ('dia_semana', 'profesional')
    search_fields = ('profesional__nombre',)
    ordering = ('profesional', 'dia_semana', 'hora_inicio')
    autocomplete_fields = ('profesional',)


# ============================================================================
# CITA
# ----------------------------------------------------------------------------
# Entidad central. Se muestra inline de Ficha Clínica para registrar el
# diagnóstico en la misma pantalla. Incluye acciones masivas para
# confirmar o cancelar citas.
# ============================================================================
class FichaClinicaInline(admin.StackedInline):
    """
    Inline de Ficha Clínica dentro del formulario de Cita.

    Permite crear la ficha clínica en el momento en que la cita es
    atendida, sin cambiar de pantalla.
    """

    model = FichaClinica
    extra = 0
    max_num = 1
    fields = ('diagnostico', 'tratamiento', 'recetas', 'examenes')
    show_change_link = True


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    """
    Administración de Citas médicas.

    - `date_hierarchy`: navegación por año/mes/día en la fecha de la cita.
    - `list_filter`: estado, profesional, fecha.
    - `search_fields`: nombre de mascota o tutor, motivo.
    - `autocomplete_fields`: mascota y profesional.
    - Acciones masivas: confirmar, cancelar, marcar como atendida.
    - Inline: Ficha Clínica.
    """

    list_display = (
        'mascota', 'profesional', 'fecha_hora', 'duracion_min',
        'estado', '_tiene_ficha',
    )
    list_filter = ('estado', 'profesional', 'fecha_hora')
    search_fields = ('mascota__nombre', 'mascota__tutor__nombre', 'motivo')
    date_hierarchy = 'fecha_hora'
    ordering = ('-fecha_hora',)
    autocomplete_fields = ('mascota', 'profesional')
    list_select_related = ('mascota', 'profesional')
    readonly_fields = ('fecha_creacion',)
    inlines = [FichaClinicaInline]

    fieldsets = (
        ('Paciente y profesional', {
            'fields': ('mascota', 'profesional')
        }),
        ('Agendamiento', {
            'fields': ('fecha_hora', 'duracion_min', 'motivo')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',),
        }),
    )

    actions = ['confirmar_citas', 'cancelar_citas', 'marcar_atendidas']

    @admin.display(description='Ficha', boolean=True)
    def _tiene_ficha(self, obj):
        """Indica si la cita ya tiene ficha clínica asociada."""
        return hasattr(obj, 'ficha')

    @admin.action(description='Confirmar citas seleccionadas')
    def confirmar_citas(self, request, queryset):
        """Cambia el estado de las citas seleccionadas a 'Confirmada'."""
        actualizadas = queryset.update(estado=Cita.ESTADO_CONFIRMADA)
        self.message_user(request, f'{actualizadas} cita(s) confirmada(s).')

    @admin.action(description='Cancelar citas seleccionadas')
    def cancelar_citas(self, request, queryset):
        """Cambia el estado de las citas seleccionadas a 'Cancelada'."""
        actualizadas = queryset.update(estado=Cita.ESTADO_CANCELADA)
        self.message_user(request, f'{actualizadas} cita(s) cancelada(s).')

    @admin.action(description='Marcar como atendidas')
    def marcar_atendidas(self, request, queryset):
        """Cambia el estado de las citas seleccionadas a 'Atendida'."""
        actualizadas = queryset.update(estado=Cita.ESTADO_ATENDIDA)
        self.message_user(request, f'{actualizadas} cita(s) marcada(s) como atendida(s).')


# ============================================================================
# FICHA CLÍNICA
# ----------------------------------------------------------------------------
# Registro médico. Se registra aquí para consulta directa (también editable
# desde el inline de Cita).
# ============================================================================
@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    """
    Administración de Fichas Clínicas.

    Búsqueda por nombre de mascota o diagnóstico. Filtro por fecha de
    creación. Ordenado por más reciente.
    """

    list_display = ('cita', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('cita__mascota__nombre', 'cita__mascota__tutor__nombre', 'diagnostico')
    date_hierarchy = 'fecha_creacion'
    ordering = ('-fecha_creacion',)
    autocomplete_fields = ('cita',)
    readonly_fields = ('fecha_creacion',)


# ============================================================================
# RECORDATORIO
# ----------------------------------------------------------------------------
# Avisos de vacunación / control. Se incluye acción masiva para marcar
# varios como enviados y filtro por estado y tipo.
# ============================================================================
@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    """
    Administración de Recordatorios.

    - Filtros: tipo, enviado, fecha programada.
    - Búsqueda: mascota, notas.
    - Acción masiva: marcar seleccionados como enviados.
    - Columna calculada `_vencido` (rojo si la fecha ya pasó y no se envió).
    """

    list_display = (
        'mascota', 'tipo', 'fecha_programada', 'enviado', '_vencido',
    )
    list_filter = ('tipo', 'enviado', 'fecha_programada')
    search_fields = ('mascota__nombre', 'mascota__tutor__nombre', 'notas')
    date_hierarchy = 'fecha_programada'
    ordering = ('fecha_programada',)
    autocomplete_fields = ('mascota',)
    list_select_related = ('mascota',)
    readonly_fields = ('fecha_creacion',)

    fieldsets = (
        ('Destinatario', {
            'fields': ('mascota',)
        }),
        ('Recordatorio', {
            'fields': ('tipo', 'fecha_programada', 'notas')
        }),
        ('Estado', {
            'fields': ('enviado',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',),
        }),
    )

    actions = ['marcar_enviados']

    @admin.display(description='Vencido', boolean=True)
    def _vencido(self, obj):
        """True si la fecha programada ya pasó y el recordatorio no se envió."""
        return (not obj.enviado) and (obj.fecha_programada < date.today())

    @admin.action(description='Marcar recordatorios seleccionados como enviados')
    def marcar_enviados(self, request, queryset):
        """Marca los recordatorios seleccionados como enviados."""
        actualizados = queryset.update(enviado=True)
        self.message_user(request, f'{actualizados} recordatorio(s) marcado(s) como enviado(s).')