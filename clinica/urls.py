"""
============================================================================
Enrutamiento de la app `clinica` — PetCare EVA3
----------------------------------------------------------------------------
Todas las rutas CRUD del sistema. Se usa app_name='clinica' para nombrar
las URLs y referenciarlas con `{% url 'clinica:xxx' %}`.
============================================================================
"""

from django.urls import path

from . import views

app_name = 'clinica'

urlpatterns = [
    # Dashboard
    path('', views.HomeView.as_view(), name='home'),

    # Tutores
    path('tutores/', views.TutorListView.as_view(), name='tutor_list'),
    path('tutores/nuevo/', views.TutorCreateView.as_view(), name='tutor_create'),
    path('tutores/<int:pk>/editar/', views.TutorUpdateView.as_view(), name='tutor_update'),
    path('tutores/<int:pk>/eliminar/', views.TutorDeleteView.as_view(), name='tutor_delete'),

    # Mascotas
    path('mascotas/', views.MascotaListView.as_view(), name='mascota_list'),
    path('mascotas/nueva/', views.MascotaCreateView.as_view(), name='mascota_create'),
    path('mascotas/<int:pk>/editar/', views.MascotaUpdateView.as_view(), name='mascota_update'),
    path('mascotas/<int:pk>/eliminar/', views.MascotaDeleteView.as_view(), name='mascota_delete'),

    # Citas
    path('citas/', views.CitaListView.as_view(), name='cita_list'),
    path('citas/nueva/', views.CitaCreateView.as_view(), name='cita_create'),
    path('citas/<int:pk>/', views.CitaDetailView.as_view(), name='cita_detail'),
    path('citas/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='cita_update'),
    path('citas/<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='cita_delete'),
    path('citas/<int:pk>/confirmar/', views.cita_confirmar_rapido, name='cita_confirmar'),

    # Fichas clínicas
    path('citas/<int:cita_pk>/ficha/nueva/', views.FichaCreateView.as_view(), name='ficha_create'),
    path('fichas/<int:pk>/editar/', views.FichaUpdateView.as_view(), name='ficha_update'),

    # Recordatorios
    path('recordatorios/', views.RecordatorioListView.as_view(), name='recordatorio_list'),
    path('recordatorios/nuevo/', views.RecordatorioCreateView.as_view(), name='recordatorio_create'),
    path('recordatorios/<int:pk>/editar/', views.RecordatorioUpdateView.as_view(), name='recordatorio_update'),
    path('recordatorios/<int:pk>/eliminar/', views.RecordatorioDeleteView.as_view(), name='recordatorio_delete'),
    path('recordatorios/<int:pk>/marcar-enviado/', views.recordatorio_marcar_enviado, name='recordatorio_marcar_enviado'),

    # API auxiliar (filtro dinámico de mascotas por tutor en el formulario de citas)
    path('api/mascotas/<int:tutor_id>/', views.api_mascotas_tutor, name='api_mascotas_tutor'),
]