"""
============================================================================
Modelos de dominio — PetCare EVA3
----------------------------------------------------------------------------
Archivo: clinica/models.py
Propósito:
    Define el modelo de datos del sistema de gestión veterinaria PetCare.
    Cubre los 4 requerimientos del caso:

        1. CRUD y administración de Tutores y Mascotas.
        2. Agendamiento de citas con disponibilidad por profesional.
        3. Ficha clínica digital (diagnósticos, tratamientos, recetas,
           exámenes).
        4. Recordatorios de vacunación y controles periódicos.

Relaciones principales:
    Tutor 1──N Mascota
    Mascota 1──N Cita N──1 Profesional
    Cita 1──1 FichaClinica
    Mascota 1──N Recordatorio
    Profesional 1──N Disponibilidad

Convenciones:
    - Todos los modelos incluyen docstring de clase y docstring por campo.
    - Los campos con choices definen tuplas nombradas en MAYÚSCULAS.
    - Las reglas de negocio se implementan en `clean()` para que se validen
      tanto en formularios como en el Admin y en DRF.
    - `verbose_name` en español para que el Admin se muestre en español.
============================================================================
"""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


# ============================================================================
# TUTOR
# ----------------------------------------------------------------------------
# Representa al dueño/responsable legal de una o más mascotas.
# Es la entidad raíz del dominio: sin tutor no hay mascota.
# ============================================================================
class Tutor(models.Model):
    """
    Tutor (dueño) de una o más mascotas.

    El RUT es único para evitar duplicidad de registros. El email también
    es único porque se usa como canal de notificación de recordatorios.
    """

    # Nombre completo del tutor (razón social o persona natural).
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre completo',
        help_text='Nombre y apellidos del tutor.',
    )

    # RUT chileno con formato 12345678-9 (sin puntos, con guion).
    rut = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='RUT',
        help_text='RUT sin puntos, con guion. Ej: 12345678-9.',
    )

    # Correo electrónico de contacto, único en el sistema.
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico',
        help_text='Se usa para notificaciones de recordatorios.',
    )

    # Teléfono de contacto (formato libre para permitir +56 9 ...).
    telefono = models.CharField(
        max_length=20,
        verbose_name='Teléfono',
        help_text='Teléfono de contacto. Ej: +56912345678.',
    )

    # Dirección física (opcional, útil para despacho o visitas).
    direccion = models.TextField(
        blank=True,
        verbose_name='Dirección',
        help_text='Dirección particular del tutor (opcional).',
    )

    # Fecha de registro en el sistema (auditoría).
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro',
    )

    class Meta:
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutores'
        ordering = ['nombre']

    def __str__(self):
        """Representación legible: 'Nombre (RUT)'."""
        return f'{self.nombre} ({self.rut})'


# ============================================================================
# MASCOTA
# ----------------------------------------------------------------------------
# Paciente del sistema. Pertenece obligatoriamente a un Tutor.
# Al eliminar un Tutor se eliminan en cascada sus mascotas.
# ============================================================================
class Mascota(models.Model):
    """
    Mascota (paciente) atendida en la clínica.

    Cada mascota pertenece a un único Tutor. Se guarda especie, raza y
    fecha de nacimiento para cálculo de edad y protocolos de vacunación.
    """

    # Especies soportadas. Se pueden ampliar en el futuro.
    ESPECIE_PERRO = 'PERRO'
    ESPECIE_GATO = 'GATO'
    ESPECIE_OTRO = 'OTRO'
    ESPECIE_CHOICES = [
        (ESPECIE_PERRO, 'Perro'),
        (ESPECIE_GATO, 'Gato'),
        (ESPECIE_OTRO, 'Otro'),
    ]

    # Nombre de la mascota.
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre',
        help_text='Nombre de la mascota.',
    )

    # Especie de la mascota.
    especie = models.CharField(
        max_length=10,
        choices=ESPECIE_CHOICES,
        default=ESPECIE_PERRO,
        verbose_name='Especie',
    )

    # Raza (opcional; puede ser mestizo).
    raza = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Raza',
        help_text='Raza de la mascota (opcional).',
    )

    # Sexo de la mascota (relevante clínicamente).
    SEXO_MACHO = 'M'
    SEXO_HEMBRA = 'H'
    SEXO_CHOICES = [
        (SEXO_MACHO, 'Macho'),
        (SEXO_HEMBRA, 'Hembra'),
    ]
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        default=SEXO_MACHO,
        verbose_name='Sexo',
    )

    # Fecha de nacimiento para calcular edad y programar controles.
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento',
    )

    # Tutor propietario. CASCADE: si se elimina el tutor, se eliminan
    # sus mascotas y, en cascada, sus citas, fichas y recordatorios.
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        related_name='mascotas',
        verbose_name='Tutor',
    )

    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['nombre']

    def __str__(self):
        """Representación legible: 'Nombre (Especie)'."""
        return f'{self.nombre} ({self.get_especie_display()})'


# ============================================================================
# PROFESIONAL
# ----------------------------------------------------------------------------
# Veterinario/a que atiende las citas. Cada profesional tiene su propia
# disponibilidad horaria (ver modelo Disponibilidad).
# ============================================================================
class Profesional(models.Model):
    """
    Profesional veterinario que atiende las citas de la clínica.
    """

    # Nombre completo del profesional.
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre completo',
    )

    # Especialidad declarada (medicina general, cirugía, dermatología, etc.).
    especialidad = models.CharField(
        max_length=100,
        verbose_name='Especialidad',
    )

    # Email profesional, único en el sistema.
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico',
    )

    # Indica si el profesional está activo para recibir citas.
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Si está desactivado no se le asignan nuevas citas.',
    )

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'
        ordering = ['nombre']

    def __str__(self):
        """Representación legible: 'Dr(a). Nombre — Especialidad'."""
        return f'Dr(a). {self.nombre} — {self.especialidad}'


# ============================================================================
# DISPONIBILIDAD
# ----------------------------------------------------------------------------
# Define el horario semanal en que cada profesional atiende. Se usa como
# regla de negocio al agendar una cita: la cita debe caer dentro de algún
# bloque de disponibilidad del profesional.
# ============================================================================
class Disponibilidad(models.Model):
    """
    Bloque de disponibilidad semanal de un profesional.

    Ejemplo: Lunes 09:00–13:00 para el Dr. Pérez.
    La validación se realiza en `Cita.clean()`.
    """

    # Días de la semana disponibles (lunes a sábado).
    DIA_LUN = 'LUN'
    DIA_MAR = 'MAR'
    DIA_MIE = 'MIE'
    DIA_JUE = 'JUE'
    DIA_VIE = 'VIE'
    DIA_SAB = 'SAB'
    DIA_CHOICES = [
        (DIA_LUN, 'Lunes'),
        (DIA_MAR, 'Martes'),
        (DIA_MIE, 'Miércoles'),
        (DIA_JUE, 'Jueves'),
        (DIA_VIE, 'Viernes'),
        (DIA_SAB, 'Sábado'),
    ]

    # Profesional al que pertenece este bloque.
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE,
        related_name='disponibilidades',
        verbose_name='Profesional',
    )

    # Día de la semana del bloque.
    dia_semana = models.CharField(
        max_length=3,
        choices=DIA_CHOICES,
        verbose_name='Día de la semana',
    )

    # Hora de inicio del bloque.
    hora_inicio = models.TimeField(
        verbose_name='Hora de inicio',
    )

    # Hora de fin del bloque.
    hora_fin = models.TimeField(
        verbose_name='Hora de fin',
    )

    class Meta:
        verbose_name = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidades'
        ordering = ['profesional', 'dia_semana', 'hora_inicio']
        # Un profesional no puede tener dos bloques idénticos el mismo día.
        constraints = [
            models.UniqueConstraint(
                fields=['profesional', 'dia_semana', 'hora_inicio', 'hora_fin'],
                name='unique_bloque_disponibilidad',
            )
        ]

    def clean(self):
        """Valida que la hora de inicio sea anterior a la hora de fin."""
        if self.hora_inicio and self.hora_fin and self.hora_inicio >= self.hora_fin:
            raise ValidationError(
                'La hora de inicio debe ser anterior a la hora de fin.'
            )

    def __str__(self):
        """Representación legible: 'Profesional — Día HH:MM-HH:MM'."""
        return (
            f'{self.profesional.nombre} — '
            f'{self.get_dia_semana_display()} '
            f'{self.hora_inicio:%H:%M}-{self.hora_fin:%H:%M}'
        )


# ============================================================================
# CITA
# ----------------------------------------------------------------------------
# Entidad central del agendamiento. Implementa la regla de negocio más
# importante del proyecto: NO permitir solapamiento de citas del mismo
# profesional.
# ============================================================================
class Cita(models.Model):
    """
    Cita médica agendada para una mascota con un profesional.

    Reglas de negocio implementadas en `clean()`:
        1. No puede solaparse con otra cita activa del mismo profesional.
        2. La cita debe caer dentro de un bloque de disponibilidad del
           profesional (día de la semana + rango horario).
        3. La fecha de la cita no puede ser en el pasado.

    Estados:
        PEND: Pendiente (agendada, sin confirmar).
        CONF: Confirmada (el tutor confirmó asistencia).
        ATEN: Atendida (la ficha clínica debe existir).
        CANC: Cancelada (no bloquea horario).
    """

    ESTADO_PENDIENTE = 'PEND'
    ESTADO_CONFIRMADA = 'CONF'
    ESTADO_ATENDIDA = 'ATEN'
    ESTADO_CANCELADA = 'CANC'
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_CONFIRMADA, 'Confirmada'),
        (ESTADO_ATENDIDA, 'Atendida'),
        (ESTADO_CANCELADA, 'Cancelada'),
    ]

    # Mascota que recibe la atención.
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='citas',
        verbose_name='Mascota',
    )

    # Profesional que atiende. PROTECT evita borrar profesionales con citas.
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.PROTECT,
        related_name='citas',
        verbose_name='Profesional',
    )

    # Fecha y hora exacta de inicio de la cita.
    fecha_hora = models.DateTimeField(
        verbose_name='Fecha y hora',
    )

    # Duración estimada de la atención en minutos (default 30).
    duracion_min = models.PositiveIntegerField(
        default=30,
        verbose_name='Duración (min)',
        help_text='Duración estimada de la atención en minutos.',
    )

    # Motivo declarado por el tutor al agendar.
    motivo = models.TextField(
        verbose_name='Motivo',
        help_text='Motivo de la consulta declarado por el tutor.',
    )

    # Estado actual de la cita.
    estado = models.CharField(
        max_length=4,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
        verbose_name='Estado',
    )

    # Fecha de creación del registro (auditoría).
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
    )

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['profesional', 'fecha_hora']),
            models.Index(fields=['estado']),
        ]

    # ------------------------------------------------------------------
    # Reglas de negocio
    # ------------------------------------------------------------------
    def clean(self):
        """
        Valida las reglas de negocio de la cita.

        Se ejecuta automáticamente al guardar desde el Admin, desde
        formularios (ModelForm) y desde DRF (Serializer con `full_clean`).

        Reglas:
            1. La fecha de la cita no puede ser en el pasado.
            2. La cita debe caer dentro de un bloque de disponibilidad
               del profesional (día + rango horario).
            3. No debe solaparse con otra cita activa del mismo
               profesional (estados PEND o CONF).

        Raises:
            ValidationError: si alguna regla no se cumple.
        """
        super().clean()

        # Sin fecha o profesional no se puede validar.
        if not self.fecha_hora or not self.profesional_id:
            return

        inicio = self.fecha_hora
        fin = inicio + timedelta(minutes=self.duracion_min)

        # --- Regla 1: no agendar en el pasado -------------------------
        from django.utils import timezone
        if inicio < timezone.now():
            raise ValidationError(
                {'fecha_hora': 'No se puede agendar una cita en el pasado.'}
            )

        # --- Regla 2: debe caer dentro de la disponibilidad -----------
        dia_semana = self._dia_semana_codigo(inicio)
        hora = inicio.time()
        disponibilidad = self.profesional.disponibilidades.filter(
            dia_semana=dia_semana,
            hora_inicio__lte=hora,
            hora_fin__gte=hora,
        )
        if not disponibilidad.exists():
            raise ValidationError(
                {
                    'fecha_hora': (
                        'El profesional no tiene disponibilidad para ese '
                        'día y hora. Configure un bloque en "Disponibilidades".'
                    )
                }
            )

        # --- Regla 3: no solapar con otra cita activa -----------------
        citas_activas = (
            Cita.objects
            .filter(
                profesional=self.profesional,
                estado__in=[self.ESTADO_PENDIENTE, self.ESTADO_CONFIRMADA],
            )
            .exclude(pk=self.pk)
        )
        for otra in citas_activas:
            otro_inicio = otra.fecha_hora
            otro_fin = otro_inicio + timedelta(minutes=otra.duracion_min)
            # Dos intervalos [inicio, fin) se solapan si:
            #   inicio < otro_fin  AND  fin > otro_inicio
            if inicio < otro_fin and fin > otro_inicio:
                raise ValidationError(
                    {
                        'fecha_hora': (
                            f'Solapamiento con cita de '
                            f'{otra.mascota.nombre} a las '
                            f'{otro_inicio:%d/%m/%Y %H:%M}.'
                        )
                    }
                )

    @staticmethod
    def _dia_semana_codigo(fecha):
        """
        Convierte un `datetime` al código de día usado en `Disponibilidad`.

        Args:
            fecha (datetime): fecha a convertir.

        Returns:
            str: uno de LUN, MAR, MIE, JUE, VIE, SAB, DOM.
        """
        return ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB', 'DOM'][fecha.weekday()]

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    @property
    def hora_fin(self):
        """Retorna la hora de término calculada a partir de la duración."""
        return self.fecha_hora + timedelta(minutes=self.duracion_min)

    def __str__(self):
        """Representación legible: 'Mascota — DD/MM/YYYY HH:MM (Estado)'."""
        return (
            f'{self.mascota.nombre} — '
            f'{self.fecha_hora:%d/%m/%Y %H:%M} '
            f'({self.get_estado_display()})'
        )


# ============================================================================
# FICHA CLÍNICA
# ----------------------------------------------------------------------------
# Registro médico de una cita atendida. Relación 1:1 con Cita: cada cita
# puede tener como máximo una ficha clínica. Al crear la ficha se dispara
# una señal que genera automáticamente un Recordatorio de control.
# ============================================================================
class FichaClinica(models.Model):
    """
    Ficha clínica digital asociada a una cita atendida.

    Contiene diagnóstico, tratamiento, recetas y exámenes. Se vincula 1:1
    con la Cita; si la cita se elimina, la ficha también (CASCADE).
    """

    # Cita asociada (OneToOne: una cita, una ficha).
    cita = models.OneToOneField(
        Cita,
        on_delete=models.CASCADE,
        related_name='ficha',
        verbose_name='Cita',
    )

    # Diagnóstico médico emitido por el profesional.
    diagnostico = models.TextField(
        verbose_name='Diagnóstico',
    )

    # Tratamiento indicado.
    tratamiento = models.TextField(
        verbose_name='Tratamiento',
    )

    # Recetas médicas (opcional).
    recetas = models.TextField(
        blank=True,
        verbose_name='Recetas',
        help_text='Medicamentos recetados (opcional).',
    )

    # Exámenes solicitados o resultados (opcional).
    examenes = models.TextField(
        blank=True,
        verbose_name='Exámenes',
        help_text='Exámenes solicitados o resultados (opcional).',
    )

    # Fecha de creación de la ficha (auditoría).
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
    )

    class Meta:
        verbose_name = 'Ficha clínica'
        verbose_name_plural = 'Fichas clínicas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        """Representación legible: 'Ficha de Mascota (DD/MM/YYYY)'."""
        return (
            f'Ficha de {self.cita.mascota.nombre} '
            f'({self.fecha_creacion:%d/%m/%Y})'
        )


# ============================================================================
# RECORDATORIO
# ----------------------------------------------------------------------------
# Aviso programado para vacunación o control periódico de una mascota.
# Se genera automáticamente al crear una FichaClinica (ver signals.py)
# y también puede crearse manualmente desde el Admin.
# ============================================================================
class Recordatorio(models.Model):
    """
    Recordatorio de vacunación o control periódico para una mascota.

    El campo `enviado` permite marcar recordatorios ya notificados, de
    modo que el dashboard de "pendientes" solo muestre los futuros.
    """

    TIPO_VACUNACION = 'VAC'
    TIPO_CONTROL = 'CTRL'
    TIPO_CHOICES = [
        (TIPO_VACUNACION, 'Vacunación'),
        (TIPO_CONTROL, 'Control periódico'),
    ]

    # Mascota a la que se le recuerda.
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='recordatorios',
        verbose_name='Mascota',
    )

    # Tipo de recordatorio.
    tipo = models.CharField(
        max_length=4,
        choices=TIPO_CHOICES,
        default=TIPO_CONTROL,
        verbose_name='Tipo',
    )

    # Fecha en que debe notificarse el recordatorio.
    fecha_programada = models.DateField(
        verbose_name='Fecha programada',
    )

    # Indica si el recordatorio ya fue notificado.
    enviado = models.BooleanField(
        default=False,
        verbose_name='Enviado',
    )

    # Notas libres (ej. "refuerzo anual", "control post-operatorio").
    notas = models.TextField(
        blank=True,
        verbose_name='Notas',
    )

    # Fecha de creación del registro (auditoría).
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
    )

    class Meta:
        verbose_name = 'Recordatorio'
        verbose_name_plural = 'Recordatorios'
        ordering = ['fecha_programada']
        indexes = [
            models.Index(fields=['enviado', 'fecha_programada']),
        ]

    def __str__(self):
        """Representación legible: 'Tipo — Mascota (DD/MM/YYYY)'."""
        return (
            f'{self.get_tipo_display()} — {self.mascota.nombre} '
            f'({self.fecha_programada:%d/%m/%Y})'
        )