"""
============================================================================
Vistas de la app `clinica` — PetCare EVA3
----------------------------------------------------------------------------
Archivo: clinica/views.py
Propósito:
    Define las vistas de la app. En la Fase 3 solo se implementa HomeView
    (protegida por login) como placeholder. Las vistas CRUD completas
    (Tutores, Mascotas, Citas, etc.) se agregan en la Fase 4.
============================================================================
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Página de inicio del sistema PetCare.

    Requiere autenticación: si el usuario no ha iniciado sesión, Django
    lo redirige automáticamente a LOGIN_URL (/accounts/login/).
    """

    template_name = 'home.html'