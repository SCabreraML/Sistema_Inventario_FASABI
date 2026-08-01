from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

from .models import (
    Carrera, CentroCosto, Bodega, ActivoFijo, CategoriaActivo, Mantenimiento, MovimientoActivo,
    CategoriaInsumo, Insumo, StockInsumo, MovimientoInsumo, Solicitud, DetalleSolicitud, Compra, Persona
)
from .forms import (
    CarreraForm, CentroCostoForm, BodegaForm, ActivoFijoForm, CategoriaActivoForm, MantenimientoForm,
    CategoriaInsumoForm, InsumoForm, StockInsumoForm, MovimientoInsumoForm, SolicitudForm, DetalleSolicitudFormSet, CompraForm
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
        'centros': centros,
        'carrera_selected': carrera_id,
        'centro_selected': centro_id,
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

    # Solicitudes recientes (Notificaciones del estado de solicitudes)
    solicitudes_recientes = Solicitud.objects.all().order_by('-fecha_solicitud')[:5]

    return render(request, 'inventario/dashboard_alertas.html', {
        'mantenimientos': proximos_mantenimientos,
        'stock_bajo': stock_bajo,
        'proximos_caducados': proximos_caducados,
        'solicitudes_recientes': solicitudes_recientes,
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


# --- SPRINT 5 VIEWS ---

# Solicitudes
class SolicitudListView(LoginRequiredMixin, ListView):
    model = Solicitud
    template_name = 'inventario/solicitud_list.html'
    context_object_name = 'solicitudes'

class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = Solicitud
    template_name = 'inventario/solicitud_detail.html'
    context_object_name = 'solicitud'

class SolicitudCreateView(LoginRequiredMixin, CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'inventario/solicitud_form.html'
    success_url = reverse_lazy('solicitud_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detalles'] = DetalleSolicitudFormSet(self.request.POST)
        else:
            data['detalles'] = DetalleSolicitudFormSet()
        data['title'] = "Crear Solicitud de Insumos"
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['detalles']
        self.object = form.save()
        if detalles.is_valid():
            detalles.instance = self.object
            detalles.save()
            messages.success(self.request, "Solicitud de insumos creada exitosamente.")
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

# Solicitud approval and rejection
@login_required
def solicitud_approve(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.estado = 'Aprobada'
    solicitud.save()
    messages.success(request, f"La solicitud {solicitud.id} ha sido aprobada.")
    return redirect('solicitud_detail', pk=pk)

@login_required
def solicitud_reject(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.estado = 'Rechazada'
    solicitud.save()
    messages.success(request, f"La solicitud {solicitud.id} ha sido rechazada.")
    return redirect('solicitud_detail', pk=pk)

# Compras
class CompraListView(LoginRequiredMixin, ListView):
    model = Compra
    template_name = 'inventario/compra_list.html'
    context_object_name = 'compras'

class CompraDetailView(LoginRequiredMixin, DetailView):
    model = Compra
    template_name = 'inventario/compra_detail.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bodegas'] = Bodega.objects.all()
        return context

class CompraCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'inventario/compra_form.html'
    success_url = reverse_lazy('compra_list')
    success_message = "Compra registrada exitosamente."

    def get_initial(self):
        initial = super().get_initial()
        solicitud_id = self.request.GET.get('solicitud')
        if solicitud_id:
            solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
            initial['solicitud'] = solicitud
            initial['estado'] = 'Pendiente'
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrar Compra"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.solicitud:
            sol = self.object.solicitud
            sol.estado = 'Comprada'
            sol.save()
        return response

# Reception of Merchandise (Intake registration)
@login_required
def compra_recibir(request, pk):
    if request.method == 'POST':
        compra = get_object_or_404(Compra, pk=pk)
        bodega_id = request.POST.get('bodega')
        if not bodega_id:
            messages.error(request, "Debe seleccionar una bodega para registrar el ingreso.")
            return redirect('compra_detail', pk=pk)

        bodega = get_object_or_404(Bodega, pk=bodega_id)

        # Update states
        compra.estado = 'Recibida'
        compra.save()

        sol = compra.solicitud
        if sol:
            sol.estado = 'Recibida'
            sol.save()

            # Create MovimientoInsumo of type INGRESO for each item in the Request
            for detalle in sol.detalles.all():
                MovimientoInsumo.objects.create(
                    insumo=detalle.insumo,
                    bodega=bodega,
                    tipo='INGRESO',
                    cantidad=detalle.cantidad_solicitada,
                    observacion=f"Ingreso automático por Compra #{compra.id} (Solicitud #{sol.id})",
                    usuario=request.user
                )
            messages.success(request, f"¡Mercadería recibida con éxito en {bodega.nombre}! Se ha actualizado el stock de los insumos correspondientes.")
        else:
            messages.success(request, "La compra ha sido marcada como Recibida.")

        return redirect('compra_detail', pk=pk)
    return redirect('compra_list')


# --- SPRINT 6 VIEWS (PDF EXPORTS) ---

@login_required
def reporte_stock_pdf(request):
    bodega_id = request.GET.get('bodega')
    stocks = StockInsumo.objects.all()
    if bodega_id:
        stocks = stocks.filter(bodega_id=bodega_id)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003B7A'),
        alignment=1,
        spaceAfter=20
    )
    normal_style = styles['Normal']
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        textColor=colors.white,
        fontSize=10
    )

    story.append(Paragraph("SISTEMA LOGÍSTICO FASABI", title_style))
    story.append(Paragraph("REPORTE DE STOCK DE INSUMOS POR BODEGA", ParagraphStyle('SubStyle', parent=styles['Heading3'], alignment=1, spaceAfter=20)))

    from django.utils import timezone
    story.append(Paragraph(f"<b>Fecha de Generación:</b> {timezone.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    story.append(Spacer(1, 15))

    data = [
        [
            Paragraph("<b>Insumo</b>", header_style),
            Paragraph("<b>Bodega</b>", header_style),
            Paragraph("<b>Cant. Actual</b>", header_style),
            Paragraph("<b>Cant. Mínima</b>", header_style),
            Paragraph("<b>Lote</b>", header_style),
            Paragraph("<b>Fecha Caducidad</b>", header_style)
        ]
    ]

    for stock in stocks:
        insumo_p = Paragraph(f"<b>{stock.insumo.nombre}</b><br/><font color='gray' size='8'>Código: {stock.insumo.codigo or '-'}</font>", normal_style)
        bodega_p = Paragraph(stock.bodega.nombre, normal_style)
        cant_actual_p = Paragraph(f"{stock.cantidad_actual} {stock.insumo.unidad_medida}", normal_style)
        cant_min_p = Paragraph(f"{stock.cantidad_minima} {stock.insumo.unidad_medida}", normal_style)
        lote_p = Paragraph(stock.lote or "-", normal_style)
        caducidad_p = Paragraph(stock.fecha_caducidad.strftime('%d/%m/%Y') if stock.fecha_caducidad else "-", normal_style)

        data.append([insumo_p, bodega_p, cant_actual_p, cant_min_p, lote_p, caducidad_p])

    t = Table(data, colWidths=[150, 100, 80, 80, 60, 70])
    ts = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003B7A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
    ]

    for i in range(1, len(data)):
        stock = stocks[i-1]
        if stock.cantidad_actual < stock.cantidad_minima:
            ts.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#FFF2F2')))

    t.setStyle(TableStyle(ts))
    story.append(t)

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_stock.pdf"'
    return response


@login_required
def reporte_activos_pdf(request):
    carrera_id = request.GET.get('carrera')
    centro_id = request.GET.get('centro')

    activos = ActivoFijo.objects.all()
    if carrera_id:
        activos = activos.filter(carrera_id=carrera_id)
    if centro_id:
        activos = activos.filter(centro_costo_id=centro_id)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003B7A'),
        alignment=1,
        spaceAfter=20
    )
    normal_style = styles['Normal']
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        textColor=colors.white,
        fontSize=10
    )

    story.append(Paragraph("SISTEMA LOGÍSTICO FASABI", title_style))
    story.append(Paragraph("REPORTE DE ACTIVOS FIJOS", ParagraphStyle('SubStyle2', parent=styles['Heading3'], alignment=1, spaceAfter=20)))

    from django.utils import timezone
    story.append(Paragraph(f"<b>Fecha de Generación:</b> {timezone.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    story.append(Spacer(1, 15))

    data = [
        [
            Paragraph("<b>Código</b>", header_style),
            Paragraph("<b>Nombre</b>", header_style),
            Paragraph("<b>Categoría</b>", header_style),
            Paragraph("<b>Carrera</b>", header_style),
            Paragraph("<b>Ubicación</b>", header_style),
            Paragraph("<b>Estado</b>", header_style)
        ]
    ]

    for activo in activos:
        codigo_p = Paragraph(activo.codigo_inventario or "-", normal_style)
        nombre_p = Paragraph(activo.nombre, normal_style)
        cat_p = Paragraph(activo.categoria_activo.nombre, normal_style)
        carrera_p = Paragraph(activo.carrera.nombre, normal_style)
        ub_p = Paragraph(activo.ubicacion_actual or "-", normal_style)
        estado_p = Paragraph(activo.estado, normal_style)

        data.append([codigo_p, nombre_p, cat_p, carrera_p, ub_p, estado_p])

    t = Table(data, colWidths=[80, 140, 90, 90, 80, 60])
    ts = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003B7A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
    ]
    t.setStyle(TableStyle(ts))
    story.append(t)

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_activos.pdf"'
    return response
