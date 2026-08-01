from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('TECNICO', 'Técnico'),
        ('CONSERJE', 'Conserje'),
        ('LABORATORIO', 'Usuario de Laboratorio'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='LABORATORIO')
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Carrera(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, blank=True, null=True)
    coordinador = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'carreras'

    def __str__(self):
        return self.nombre

class CentroCosto(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='centros_costo')
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=30, blank=True, null=True)
    responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='centros_responsable')
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'centros_costo'

    def __str__(self):
        return self.nombre

class Bodega(models.Model):
    TIPO_BODEGA_CHOICES = (
        ('910_Vigentes', '910 Vigentes'),
        ('Uso_Diario', 'Uso Diario'),
        ('Caducados', 'Caducados'),
        ('Limpieza', 'Limpieza'),
    )
    nombre = models.CharField(max_length=100)
    tipo_bodega = models.CharField(max_length=50, choices=TIPO_BODEGA_CHOICES)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'bodegas'

    def __str__(self):
        return self.nombre

class CategoriaActivo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias_activos'

    def __str__(self):
        return self.nombre

class ActivoFijo(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.SET_NULL, null=True, blank=True)
    categoria_activo = models.ForeignKey(CategoriaActivo, on_delete=models.CASCADE)
    codigo_inventario = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    valor_adquisicion = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    fecha_adquisicion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, default='Operativo')
    ubicacion_actual = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'activos_fijos'

    def __str__(self):
        return f"{self.nombre} ({self.codigo_inventario})"

class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias_insumos'

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    categoria_insumo = models.ForeignKey(CategoriaInsumo, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=20)
    es_perecedero = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'insumos'

    def __str__(self):
        return self.nombre

class StockInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cantidad_minima = models.DecimalField(max_digits=12, decimal_places=2, default=5)
    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_caducidad = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_insumos'
        unique_together = ('insumo', 'bodega')

    def __str__(self):
        return f"{self.insumo.nombre} - {self.bodega.nombre}: {self.cantidad_actual}"

class Persona(models.Model):
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'personas'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Solicitud(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.SET_NULL, null=True, blank=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, default='Pendiente')
    observacion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'solicitudes'

    def __str__(self):
        return f"Solicitud {self.id} - {self.persona}"

class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='detalles')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad_solicitada = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detalle_solicitud'

class Compra(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_compra = models.DateField()
    proveedor = models.CharField(max_length=200, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=30, default='Recibida')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'compras'

class Mantenimiento(models.Model):
    activo_fijo = models.ForeignKey(ActivoFijo, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    estado = models.CharField(max_length=30, default='Programado')

    class Meta:
        db_table = 'mantenimientos'

class MovimientoActivo(models.Model):
    TIPOS = (
        ('ASIGNACION', 'Asignación'),
        ('DEVOLUCION', 'Devolución'),
        ('TRASLADO', 'Traslado'),
        ('BAJA', 'Baja'),
    )
    activo_fijo = models.ForeignKey(ActivoFijo, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha = models.DateTimeField(auto_now_add=True)
    persona = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True)
    ubicacion_anterior = models.CharField(max_length=150, blank=True, null=True)
    ubicacion_nueva = models.CharField(max_length=150, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'movimientos_activos'

@receiver(pre_save, sender=ActivoFijo)
def track_asset_movement(sender, instance, **kwargs):
    if instance.pk:
        old_instance = ActivoFijo.objects.get(pk=instance.pk)
        if old_instance.ubicacion_actual != instance.ubicacion_actual:
            MovimientoActivo.objects.create(
                activo_fijo=instance,
                tipo='TRASLADO',
                ubicacion_anterior=old_instance.ubicacion_actual,
                ubicacion_nueva=instance.ubicacion_actual,
                observacion='Cambio automático de ubicación'
            )
