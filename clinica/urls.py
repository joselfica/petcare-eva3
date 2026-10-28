"""
============================================================================
Enrutamiento de la app `clinica` — PetCare EVA3
----------------------------------------------------------------------------
Archivo: clinica/urls.py
Propósito:
    Define las rutas de la app de dominio. En la Fase 3 solo se expone
    una vista "home" mínima para evitar errores de importación; las rutas
    CRUD completas se agregan en la Fase 4.
============================================================================
"""

from django.urls import path

from . import views

app_name = 'clinica'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]