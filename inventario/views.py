from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F

from .models import (
    Carrera, CentroCosto, Bodega, ActivoFijo, CategoriaActivo, Mantenimiento, MovimientoActivo,
    CategoriaInsumo, Insumo, StockInsumo, MovimientoInsumo
)
from .forms import (
    CarreraForm, CentroCostoForm, BodegaForm, ActivoFijoForm, CategoriaActivoForm, MantenimientoForm,
    CategoriaInsumoForm, InsumoForm, StockInsumoForm, MovimientoInsumoForm
)

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

# Historial de Movimientos de Activos
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

    # Alertas de stock bajo
    stock_bajo = StockInsumo.objects.filter(cantidad_actual__lt=F('cantidad_minima'))

    # Alertas de caducidad (próximos 30 días)
    hoy = timezone.now().date()
    proximos_caducados = StockInsumo.objects.filter(
        insumo__es_perecedero=True,
        fecha_caducidad__lte=hoy + timedelta(days=30)
    ).order_by('fecha_caducidad')

    return render(request, 'inventario/dashboard_alertas.html', {
        'mantenimientos': proximos_mantenimientos,
        'stock_bajo': stock_bajo,
        'proximos_caducados': proximos_caducados,
    })

# --- SPRINT 4 VIEWS ---

# Categoria Insumo Views
class CategoriaInsumoListView(LoginRequiredMixin, ListView):
    model = CategoriaInsumo
    template_name = 'inventario/categoria_insumo_list.html'
    context_object_name = 'categorias'

class CategoriaInsumoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CategoriaInsumo
    form_class = CategoriaInsumoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('categoria_insumo_list')
    success_message = "Categoría de Insumo creada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear Categoría de Insumo"
        return context

class CategoriaInsumoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CategoriaInsumo
    form_class = CategoriaInsumoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('categoria_insumo_list')
    success_message = "Categoría de Insumo actualizada exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Categoría de Insumo"
        return context

# Insumo Views
class InsumoListView(LoginRequiredMixin, ListView):
    model = Insumo
    template_name = 'inventario/insumo_list.html'
    context_object_name = 'insumos'

class InsumoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('insumo_list')
    success_message = "Insumo registrado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrar Insumo"
        return context

class InsumoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('insumo_list')
    success_message = "Insumo actualizado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Insumo"
        return context

# StockInsumo Views
class StockInsumoListView(LoginRequiredMixin, ListView):
    model = StockInsumo
    template_name = 'inventario/stock_insumo_list.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        queryset = super().get_queryset()
        bodega_id = self.request.GET.get('bodega')
        if bodega_id:
            queryset = queryset.filter(bodega_id=bodega_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bodegas'] = Bodega.objects.all()
        context['selected_bodega'] = self.request.GET.get('bodega')
        return context

class StockInsumoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StockInsumo
    form_class = StockInsumoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('stock_insumo_list')
    success_message = "Stock registrado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrar Stock de Insumo"
        return context

class StockInsumoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StockInsumo
    form_class = StockInsumoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('stock_insumo_list')
    success_message = "Stock actualizado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Stock de Insumo"
        return context

# MovimientoInsumo Views
class MovimientoInsumoListView(LoginRequiredMixin, ListView):
    model = MovimientoInsumo
    template_name = 'inventario/movimiento_insumo_list.html'
    context_object_name = 'movimientos'

class MovimientoInsumoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MovimientoInsumo
    form_class = MovimientoInsumoForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('movimiento_insumo_list')
    success_message = "Movimiento de Insumo registrado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrar Movimiento de Insumo"
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
