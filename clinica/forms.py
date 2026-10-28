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
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'tutor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tutor': forms.Select(attrs={'class': 'form-select'}),
        }


class CitaForm(forms.ModelForm):
    """
    Formulario de creación/edición de Citas.

    La validación de `Cita.clean()` (no pasado, dentro de disponibilidad,
    sin solapamiento) se ejecuta automáticamente al llamar `form.is_valid()`
    porque ModelForm invoca `instance.full_clean()`.
    """

    class Meta:
        model = Cita
        fields = ['mascota', 'profesional', 'fecha_hora', 'duracion_min', 'motivo', 'estado']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-select'}),
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