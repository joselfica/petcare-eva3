"""
============================================================================
Vistas de la app `clinica` — PetCare EVA3
----------------------------------------------------------------------------
Archivo: clinica/views.py
Propósito:
    Implementa las vistas del sistema PetCare con CBV:
        - HomeView (dashboard con KPIs y recordatorios).
        - CRUD de Tutores, Mascotas, Citas, Fichas Clínicas y Recordatorios.

Seguridad:
    Todas las vistas heredan de LoginRequiredMixin. La validación de
    reglas de negocio de Cita se dispara automáticamente vía ModelForm
    (que llama full_clean()).
============================================================================
"""

from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView,
)

from .forms import (
    CitaForm, FichaClinicaForm, MascotaForm, RecordatorioForm, TutorForm,
)
from .models import (
    Cita, FichaClinica, Mascota, Recordatorio, Tutor,
)


# ============================================================================
# HOME / DASHBOARD
# ============================================================================
class HomeView(LoginRequiredMixin, TemplateView):
    """Dashboard con KPIs y recordatorios próximos."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = date.today()
        ctx['today'] = hoy
        ctx['total_tutores'] = Tutor.objects.count()
        ctx['total_mascotas'] = Mascota.objects.count()
        ctx['citas_hoy'] = Cita.objects.filter(fecha_hora__date=hoy).count()
        ctx['citas_pendientes'] = Cita.objects.filter(estado=Cita.ESTADO_PENDIENTE).count()
        ctx['recordatorios_pendientes'] = (
            Recordatorio.objects
            .filter(enviado=False, fecha_programada__lte=hoy + timedelta(days=30))
            .select_related('mascota')
            .order_by('fecha_programada')[:10]
        )
        ctx['proximas_citas'] = (
            Cita.objects
            .filter(
                estado__in=[Cita.ESTADO_PENDIENTE, Cita.ESTADO_CONFIRMADA],
                fecha_hora__date__gte=hoy,
                fecha_hora__date__lte=hoy + timedelta(days=7),
            )
            .select_related('mascota', 'profesional')
            .order_by('fecha_hora')
        )
        return ctx


# ============================================================================
# TUTOR — CRUD
# ============================================================================
class TutorListView(LoginRequiredMixin, ListView):
    model = Tutor
    template_name = 'clinica/tutor_list.html'
    context_object_name = 'tutores'
    paginate_by = 20


class TutorCreateView(LoginRequiredMixin, CreateView):
    model = Tutor
    form_class = TutorForm
    template_name = 'clinica/tutor_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nuevo Tutor'
        ctx['submit_label'] = 'Crear tutor'
        ctx['cancel_url'] = reverse('clinica:tutor_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Tutor creado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:tutor_list')


class TutorUpdateView(LoginRequiredMixin, UpdateView):
    model = Tutor
    form_class = TutorForm
    template_name = 'clinica/tutor_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar Tutor: {self.object.nombre}'
        ctx['submit_label'] = 'Guardar cambios'
        ctx['cancel_url'] = reverse('clinica:tutor_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Tutor actualizado.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:tutor_list')


class TutorDeleteView(LoginRequiredMixin, DeleteView):
    model = Tutor
    template_name = '_confirm_delete.html'
    success_url = reverse_lazy('clinica:tutor_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['objeto'] = self.object
        ctx['cancel_url'] = reverse('clinica:tutor_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Tutor eliminado.')
        return super().form_valid(form)


# ============================================================================
# MASCOTA — CRUD
# ============================================================================
class MascotaListView(LoginRequiredMixin, ListView):
    model = Mascota
    template_name = 'clinica/mascota_list.html'
    context_object_name = 'mascotas'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().select_related('tutor')


class MascotaCreateView(LoginRequiredMixin, CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'clinica/mascota_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nueva Mascota'
        ctx['submit_label'] = 'Crear mascota'
        ctx['cancel_url'] = reverse('clinica:mascota_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Mascota creada.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:mascota_list')


class MascotaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = 'clinica/mascota_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar Mascota: {self.object.nombre}'
        ctx['submit_label'] = 'Guardar cambios'
        ctx['cancel_url'] = reverse('clinica:mascota_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Mascota actualizada.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:mascota_list')


class MascotaDeleteView(LoginRequiredMixin, DeleteView):
    model = Mascota
    template_name = '_confirm_delete.html'
    success_url = reverse_lazy('clinica:mascota_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['objeto'] = self.object
        ctx['cancel_url'] = reverse('clinica:mascota_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Mascota eliminada.')
        return super().form_valid(form)


# ============================================================================
# CITA — CRUD + REGLAS DE NEGOCIO
# ============================================================================
class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'clinica/cita_list.html'
    context_object_name = 'citas'
    paginate_by = 20

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('mascota', 'profesional')
            .order_by('-fecha_hora')
        )


class CitaCreateView(LoginRequiredMixin, CreateView):
    """
    Crear cita. La validación anti-solapamiento / disponibilidad / fecha
    pasada se dispara automáticamente porque `CitaForm` es un ModelForm
    y Django llama `instance.full_clean()` antes de guardar.
    """

    model = Cita
    form_class = CitaForm
    template_name = 'clinica/cita_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nueva Cita'
        ctx['submit_label'] = 'Agendar cita'
        ctx['cancel_url'] = reverse('clinica:cita_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Cita agendada correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:cita_list')


class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'clinica/cita_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar Cita: {self.object}'
        ctx['submit_label'] = 'Guardar cambios'
        ctx['cancel_url'] = reverse('clinica:cita_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Cita actualizada.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:cita_list')


class CitaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una cita con su ficha clínica si existe."""

    model = Cita
    template_name = 'clinica/cita_detail.html'
    context_object_name = 'cita'

    def get_queryset(self):
        return super().get_queryset().select_related('mascota', 'profesional')


class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = '_confirm_delete.html'
    success_url = reverse_lazy('clinica:cita_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['objeto'] = self.object
        ctx['cancel_url'] = reverse('clinica:cita_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Cita eliminada.')
        return super().form_valid(form)


# ============================================================================
# FICHA CLÍNICA — Crear / Editar (asociada a una Cita)
# ============================================================================
class FichaCreateView(LoginRequiredMixin, CreateView):
    """
    Crea la ficha clínica de una cita. Al guardar, la señal
    `crear_recordatorio_control` (signals.py) genera automáticamente un
    Recordatorio de control a 180 días.
    """

    model = FichaClinica
    form_class = FichaClinicaForm
    template_name = 'clinica/ficha_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.cita = get_object_or_404(Cita, pk=kwargs['cita_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Ficha clínica — {self.cita.mascota.nombre}'
        ctx['submit_label'] = 'Guardar ficha'
        ctx['cancel_url'] = reverse('clinica:cita_detail', args=[self.cita.pk])
        return ctx

    def form_valid(self, form):
        form.instance.cita = self.cita
        messages.success(self.request, 'Ficha clínica guardada. Se generó un recordatorio de control.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:cita_detail', args=[self.cita.pk])


class FichaUpdateView(LoginRequiredMixin, UpdateView):
    model = FichaClinica
    form_class = FichaClinicaForm
    template_name = 'clinica/ficha_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar ficha — {self.object.cita.mascota.nombre}'
        ctx['submit_label'] = 'Guardar cambios'
        ctx['cancel_url'] = reverse('clinica:cita_detail', args=[self.object.cita.pk])
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Ficha clínica actualizada.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:cita_detail', args=[self.object.cita.pk])


# ============================================================================
# RECORDATORIO — Listar / Crear / Editar / Eliminar / Marcar enviado
# ============================================================================
class RecordatorioListView(LoginRequiredMixin, ListView):
    model = Recordatorio
    template_name = 'clinica/recordatorio_list.html'
    context_object_name = 'recordatorios'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('mascota', 'mascota__tutor')
        filtro = self.request.GET.get('filtro', '')
        if filtro == 'pendientes':
            qs = qs.filter(enviado=False)
        elif filtro == 'vencidos':
            qs = qs.filter(enviado=False, fecha_programada__lt=date.today())
        return qs.order_by('fecha_programada')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['hoy'] = date.today()
        ctx['filtro'] = self.request.GET.get('filtro', '')
        return ctx


class RecordatorioCreateView(LoginRequiredMixin, CreateView):
    model = Recordatorio
    form_class = RecordatorioForm
    template_name = 'clinica/recordatorio_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nuevo Recordatorio'
        ctx['submit_label'] = 'Crear recordatorio'
        ctx['cancel_url'] = reverse('clinica:recordatorio_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Recordatorio creado.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:recordatorio_list')


class RecordatorioUpdateView(LoginRequiredMixin, UpdateView):
    model = Recordatorio
    form_class = RecordatorioForm
    template_name = 'clinica/recordatorio_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar Recordatorio: {self.object}'
        ctx['submit_label'] = 'Guardar cambios'
        ctx['cancel_url'] = reverse('clinica:recordatorio_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Recordatorio actualizado.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinica:recordatorio_list')


class RecordatorioDeleteView(LoginRequiredMixin, DeleteView):
    model = Recordatorio
    template_name = '_confirm_delete.html'
    success_url = reverse_lazy('clinica:recordatorio_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['objeto'] = self.object
        ctx['cancel_url'] = reverse('clinica:recordatorio_list')
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Recordatorio eliminado.')
        return super().form_valid(form)


def recordatorio_marcar_enviado(request, pk):
    """
    Acción rápida: marca un recordatorio como enviado y vuelve al listado.

    Se implementa como función (no CBV) porque es una acción puntual de
    POST sobre un recurso. Requiere autenticación.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method != 'POST':
        return redirect('clinica:recordatorio_list')
    recordatorio = get_object_or_404(Recordatorio, pk=pk)
    recordatorio.enviado = True
    recordatorio.save()
    messages.success(request, 'Recordatorio marcado como enviado.')
    return redirect('clinica:recordatorio_list')