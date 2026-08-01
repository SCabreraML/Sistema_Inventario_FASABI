from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Carrera, CentroCosto, Bodega, CategoriaActivo,
    ActivoFijo, CategoriaInsumo, Insumo, StockInsumo,
    Persona, Solicitud, DetalleSolicitud, Compra, Mantenimiento
)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol', 'telefono')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol', 'telefono')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('rol', 'is_staff', 'is_active')

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'coordinador', 'activo')
    search_fields = ('nombre', 'codigo', 'coordinador')
    list_filter = ('activo',)

@admin.register(CentroCosto)
class CentroCostoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'carrera', 'activo')
    search_fields = ('nombre', 'codigo')
    list_filter = ('carrera', 'activo')

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_bodega', 'ubicacion', 'activo')
    search_fields = ('nombre', 'tipo_bodega')
    list_filter = ('tipo_bodega', 'activo')

@admin.register(CategoriaActivo)
class CategoriaActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created_at')
    search_fields = ('nombre',)

@admin.register(ActivoFijo)
class ActivoFijoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_inventario', 'carrera', 'categoria_activo', 'estado', 'activo')
    search_fields = ('nombre', 'codigo_inventario', 'descripcion')
    list_filter = ('carrera', 'categoria_activo', 'estado', 'activo')

@admin.register(CategoriaInsumo)
class CategoriaInsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created_at')
    search_fields = ('nombre',)

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'categoria_insumo', 'unidad_medida', 'es_perecedero', 'activo')
    search_fields = ('nombre', 'codigo')
    list_filter = ('categoria_insumo', 'es_perecedero', 'activo')

@admin.register(StockInsumo)
class StockInsumoAdmin(admin.ModelAdmin):
    list_display = ('insumo', 'bodega', 'cantidad_actual', 'cantidad_minima', 'updated_at')
    search_fields = ('insumo__nombre', 'bodega__nombre', 'lote')
    list_filter = ('bodega',)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'email', 'rol', 'activo')
    search_fields = ('nombres', 'apellidos', 'email')
    list_filter = ('rol', 'activo')

class DetalleSolicitudInline(admin.TabularInline):
    model = DetalleSolicitud
    extra = 1

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'persona', 'carrera', 'fecha_solicitud', 'estado')
    search_fields = ('persona__nombres', 'persona__apellidos', 'observacion')
    list_filter = ('estado', 'carrera', 'fecha_solicitud')
    inlines = [DetalleSolicitudInline]

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_compra', 'proveedor', 'monto_total', 'estado')
    search_fields = ('proveedor', 'estado')
    list_filter = ('estado', 'fecha_compra')

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('activo_fijo', 'persona', 'tipo', 'fecha_programada', 'estado')
    search_fields = ('activo_fijo__nombre', 'persona__nombres', 'descripcion')
    list_filter = ('tipo', 'estado', 'fecha_programada')
