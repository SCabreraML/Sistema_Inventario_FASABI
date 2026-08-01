from django import forms
from .models import Carrera, CentroCosto, Bodega, ActivoFijo, Insumo, CategoriaActivo, CategoriaInsumo, Mantenimiento, StockInsumo, MovimientoActivo, MovimientoInsumo

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre', 'codigo', 'coordinador', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'coordinador': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CentroCostoForm(forms.ModelForm):
    class Meta:
        model = CentroCosto
        fields = ['carrera', 'nombre', 'codigo', 'responsable', 'descripcion', 'activo']
        widgets = {
            'carrera': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['nombre', 'tipo_bodega', 'ubicacion', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_bodega': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoriaActivoForm(forms.ModelForm):
    class Meta:
        model = CategoriaActivo
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ActivoFijoForm(forms.ModelForm):
    class Meta:
        model = ActivoFijo
        fields = [
            'carrera', 'centro_costo', 'categoria_activo', 'codigo_inventario',
            'nombre', 'descripcion', 'valor_adquisicion', 'fecha_adquisicion',
            'estado', 'ubicacion_actual', 'activo'
        ]
        widgets = {
            'carrera': forms.Select(attrs={'class': 'form-select'}),
            'centro_costo': forms.Select(attrs={'class': 'form-select'}),
            'categoria_activo': forms.Select(attrs={'class': 'form-select'}),
            'codigo_inventario': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valor_adquisicion': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_adquisicion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion_actual': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = [
            'activo_fijo', 'persona', 'tipo', 'fecha_programada',
            'fecha_realizada', 'descripcion', 'estado'
        ]
        widgets = {
            'activo_fijo': forms.Select(attrs={'class': 'form-select'}),
            'persona': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_programada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_realizada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoriaInsumoForm(forms.ModelForm):
    class Meta:
        model = CategoriaInsumo
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['categoria_insumo', 'codigo', 'nombre', 'descripcion', 'unidad_medida', 'es_perecedero', 'activo']
        widgets = {
            'categoria_insumo': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'es_perecedero': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StockInsumoForm(forms.ModelForm):
    class Meta:
        model = StockInsumo
        fields = ['insumo', 'bodega', 'cantidad_actual', 'cantidad_minima', 'lote', 'fecha_caducidad']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

from django.forms import inlineformset_factory
from .models import Solicitud, DetalleSolicitud, Compra

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['carrera', 'centro_costo', 'persona', 'observacion']
        widgets = {
            'carrera': forms.Select(attrs={'class': 'form-select'}),
            'centro_costo': forms.Select(attrs={'class': 'form-select'}),
            'persona': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DetalleSolicitudForm(forms.ModelForm):
    class Meta:
        model = DetalleSolicitud
        fields = ['insumo', 'cantidad_solicitada']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

DetalleSolicitudFormSet = inlineformset_factory(
    Solicitud,
    DetalleSolicitud,
    form=DetalleSolicitudForm,
    extra=3,
    can_delete=True
)

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['solicitud', 'fecha_compra', 'proveedor', 'monto_total', 'estado']
        widgets = {
            'solicitud': forms.Select(attrs={'class': 'form-select'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class MovimientoInsumoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInsumo
        fields = ['insumo', 'bodega', 'tipo', 'cantidad', 'observacion']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')
        insumo = cleaned_data.get('insumo')
        bodega = cleaned_data.get('bodega')

        if tipo == 'EGRESO' and cantidad and insumo and bodega:
            try:
                stock = StockInsumo.objects.get(insumo=insumo, bodega=bodega)
                if stock.cantidad_actual < cantidad:
                    raise forms.ValidationError(
                        f"Stock insuficiente en la bodega {bodega.nombre}. Stock actual: {stock.cantidad_actual}."
                    )
            except StockInsumo.DoesNotExist:
                raise forms.ValidationError(
                    f"No existe stock registrado para {insumo.nombre} en {bodega.nombre}."
                )
        return cleaned_data
