from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Carrera, CentroCosto, Bodega, ActivoFijo, CategoriaActivo, Mantenimiento, MovimientoActivo
from .forms import CarreraForm, CentroCostoForm, BodegaForm, ActivoFijoForm, CategoriaActivoForm, MantenimientoForm

@login_required
def inicio(request):
    return render(request, 'inventario/inicio.html')

# Carrera Views
class CarreraListView(LoginRequiredMixin, ListView):
    model = Carrera
    template_name = 'inventario/carrera_list.html'
    context_object_name = 'carreras'

class CarreraCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('carrera_list')
    success_message = "Carrera creada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Carrera"
        return context

class CarreraUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('carrera_list')
    success_message = "Carrera actualizada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Carrera"
        return context

# Centro Costo Views
class CentroCostoListView(LoginRequiredMixin, ListView):
    model = CentroCosto
    template_name = 'inventario/centro_costo_list.html'
    context_object_name = 'centros'

class CentroCostoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CentroCosto
    form_class = CentroCostoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('centro_costo_list')
    success_message = "Centro de Costo creado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Centro de Costo"
        return context

class CentroCostoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CentroCosto
    form_class = CentroCostoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('centro_costo_list')
    success_message = "Centro de Costo actualizado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Centro de Costo"
        return context

# Bodega Views
class BodegaListView(LoginRequiredMixin, ListView):
    model = Bodega
    template_name = 'inventario/bodega_list.html'
    context_object_name = 'bodegas'

class BodegaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Bodega
    form_class = BodegaForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('bodega_list')
    success_message = "Bodega creada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Bodega"
        return context

class BodegaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Bodega
    form_class = BodegaForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('bodega_list')
    success_message = "Bodega actualizada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Bodega"
        return context

# Activo Fijo Views
class ActivoFijoListView(LoginRequiredMixin, ListView):
    model = ActivoFijo
    template_name = 'inventario/activo_list.html'
    context_object_name = 'activos'

class ActivoFijoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ActivoFijo
    form_class = ActivoFijoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('activo_list')
    success_message = "Activo Fijo registrado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrar Activo Fijo"
        return context

class ActivoFijoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ActivoFijo
    form_class = ActivoFijoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('activo_list')
    success_message = "Activo Fijo actualizado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Activo Fijo"
        return context

# Categoria Activo Views
class CategoriaActivoListView(LoginRequiredMixin, ListView):
    model = CategoriaActivo
    template_name = 'inventario/categoria_activo_list.html'
    context_object_name = 'categorias'

class CategoriaActivoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CategoriaActivo
    form_class = CategoriaActivoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('categoria_activo_list')
    success_message = "Categoría creada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Categoría de Activo"
        return context

# Mantenimiento Views
class MantenimientoListView(LoginRequiredMixin, ListView):
    model = Mantenimiento
    template_name = 'inventario/mantenimiento_list.html'
    context_object_name = 'mantenimientos'

class MantenimientoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('mantenimiento_list')
    success_message = "Mantenimiento programado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Programar Mantenimiento"
        return context

# Historial de Movimientos
class MovimientoActivoListView(LoginRequiredMixin, ListView):
    model = MovimientoActivo
    template_name = 'inventario/movimiento_activo_list.html'
    context_object_name = 'movimientos'

# Reportes y Alertas
@login_required
def reportes_activos(request):
    carrera_id = request.GET.get('carrera')
    centro_id = request.GET.get('centro')

    activos = ActivoFijo.objects.all()
    if carrera_id:
        activos = activos.filter(carrera_id=carrera_id)
    if centro_id:
        activos = activos.filter(centro_costo_id=centro_id)

    carreras = Carrera.objects.all()
    centros = CentroCosto.objects.all()

    return render(request, 'inventario/reporte_activos.html', {
        'activos': activos,
        'carreras': carreras,
        'centros': centros
    })

@login_required
def dashboard_alertas(request):
    from django.utils import timezone
    from datetime import timedelta

    # Alertas de mantenimiento (próximos 7 días)
    proximos_mantenimientos = Mantenimiento.objects.filter(
        fecha_programada__lte=timezone.now() + timedelta(days=7),
        estado='Programado'
    )

    # Alertas de stock bajo (se implementará en Sprint 4, pero dejamos la estructura)

    return render(request, 'inventario/dashboard_alertas.html', {
        'mantenimientos': proximos_mantenimientos
    })
