"""
============================================================================
Enrutamiento raíz del proyecto — PetCare EVA3
----------------------------------------------------------------------------
Archivo: petcare/urls.py
Propósito:
    Define las rutas de nivel superior del proyecto:
        - /admin/            → Django Admin
        - /accounts/login/   → Vista de login (template propio)
        - /accounts/logout/  → Vista de logout
        - /                  → App de dominio `clinica` (se completa en Fase 4)

Notas:
    - Se usan las vistas nativas de Django para login/logout, con
      templates personalizados en `templates/registration/`.
    - `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL` se configuraron en
      `settings.py` (Fase 0).
============================================================================
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # Autenticación (login/logout) con templates propios
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(template_name='registration/logged_out.html'),
        name='logout',
    ),

    # App de dominio (se completa en Fase 4)
    path('', include('clinica.urls')),
]