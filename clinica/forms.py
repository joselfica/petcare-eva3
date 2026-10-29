"""
============================================================================
Formularios de la app `clinica` — PetCare EVA3
----------------------------------------------------------------------------
Archivo: clinica/forms.py
Propósito:
    Define los ModelForm de cada entidad. Los formularios heredan la
    validación de `Model.clean()` automáticamente, por lo que las reglas
    de negocio de `Cita.clean()` se disparan al enviar el formulario de
    creación/edición de cita.
============================================================================
"""

from django import forms

from .models import (
    Cita,
    FichaClinica,
    Mascota,
    Profesional,
    Recordatorio,
    Tutor,
)


class TutorForm(forms.ModelForm):
    """Formulario de creación/edición de Tutores."""

    class Meta:
        model = Tutor
        fields = ['nombre', 'rut', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class MascotaForm(forms.ModelForm):
    """Formulario de creación/edición de Mascotas."""

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'sexo', 'fecha_nacimiento', 'tutor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Rocky, Michi...'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Labrador, Mestizo...'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d',
            ),
            'tutor': forms.Select(attrs={'class': 'form-select'}),
        }


class CitaForm(forms.ModelForm):
    """
    Formulario de creación/edición de Citas.

    La validación de `Cita.clean()` (no pasado, dentro de disponibilidad,
    sin solapamiento) se ejecuta automáticamente al llamar `form.is_valid()`
    porque ModelForm invoca `instance.full_clean()`.

    Incluye un campo virtual `tutor` (no se guarda en BD) que se usa en el
    frontend para filtrar el desplegable de mascotas.
    """

    tutor = forms.ModelChoiceField(
        queryset=Tutor.objects.all(),
        required=False,
        label="Tutor (Filtro)",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_tutor_filtro'}),
    )

    class Meta:
        model = Cita
        fields = ['tutor', 'mascota', 'profesional', 'fecha_hora', 'duracion_min', 'motivo', 'estado']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-select', 'id': 'id_mascota'}),
            'profesional': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'duracion_min': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'step': 5}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formato requerido por <input type="datetime-local">
        self.fields['fecha_hora'].input_formats = ['%Y-%m-%dT%H:%M']
        # Solo profesionales activos en el desplegable
        self.fields['profesional'].queryset = Profesional.objects.filter(activo=True)

        # Queryset base de mascotas: vacío en creación (se llena según el tutor)
        mascotas = Mascota.objects.none()

        # Edición: precargar tutor y sus mascotas
        if self.instance.pk:
            tutor_actual = self.instance.mascota.tutor
            self.fields['tutor'].initial = tutor_actual
            mascotas = Mascota.objects.filter(tutor=tutor_actual)

        # POST: el queryset debe contener la mascota enviada, o la validación
        # del campo fallará aunque el JS la haya cargado en el <select>.
        if self.is_bound:
            tutor_id = self.data.get(self.add_prefix('tutor'))
            if tutor_id and str(tutor_id).isdigit():
                mascotas = Mascota.objects.filter(tutor_id=tutor_id)
            else:
                # Sin tutor en el POST: se acepta cualquier mascota válida y
                # clean() deduce el tutor a partir de ella.
                mascotas = Mascota.objects.all()

        self.fields['mascota'].queryset = mascotas

    def clean(self):
        cleaned_data = super().clean()
        tutor = cleaned_data.get('tutor')
        mascota = cleaned_data.get('mascota')

        if mascota:
            if not tutor:
                # Si el campo tutor no llegó, se obtiene desde la mascota
                cleaned_data['tutor'] = mascota.tutor
            elif mascota.tutor_id != tutor.pk:
                # Seguridad extra: la mascota debe pertenecer al tutor elegido
                self.add_error('mascota', 'La mascota seleccionada no pertenece a este tutor.')

        return cleaned_data


class FichaClinicaForm(forms.ModelForm):
    """Formulario de creación/edición de Fichas Clínicas."""

    class Meta:
        model = FichaClinica
        fields = ['diagnostico', 'tratamiento', 'recetas', 'examenes']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recetas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'examenes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class RecordatorioForm(forms.ModelForm):
    """Formulario de creación/edición de Recordatorios."""

    class Meta:
        model = Recordatorio
        fields = ['mascota', 'tipo', 'fecha_programada', 'notas']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_programada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }