"""
============================================================================
Configuración de la aplicación `clinica`
----------------------------------------------------------------------------
Archivo: clinica/apps.py
Propósito:
    Define la configuración de la app de dominio PetCare. El método
    `ready()` registra las señales de Django (generación automática de
    recordatorios al crear una ficha clínica).
============================================================================
"""

from django.apps import AppConfig


class ClinicaConfig(AppConfig):
    """Configuración de la aplicación de dominio PetCare."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinica'
    verbose_name = 'Gestión Clínica Veterinaria'

    def ready(self):
        """
        Hook ejecutado al iniciar Django.

        Importa `clinica.signals` para registrar los receivers definidos
        allí. Se hace aquí para evitar importaciones circulares con
        models.py.
        """
        import clinica.signals  # noqa: F401