from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from decimal import Decimal
from inventario.models import (
    Carrera, CentroCosto, Bodega, CategoriaActivo, ActivoFijo,
    CategoriaInsumo, Insumo, StockInsumo, Persona, Solicitud,
    DetalleSolicitud, Compra, Mantenimiento, MovimientoInsumo
)

User = get_user_model()

class Command(BaseCommand):
    help = "Carga un conjunto completo de datos de ejemplo para presentar y probar la plataforma."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Limpiando datos existentes..."))

        # Clear existing data to avoid unique/foreign key conflicts and maintain pristine state
        Mantenimiento.objects.all().delete()
        MovimientoInsumo.objects.all().delete()
        StockInsumo.objects.all().delete()
        DetalleSolicitud.objects.all().delete()
        Compra.objects.all().delete()
        Solicitud.objects.all().delete()
        ActivoFijo.objects.all().delete()
        CategoriaActivo.objects.all().delete()
        Insumo.objects.all().delete()
        CategoriaInsumo.objects.all().delete()
        CentroCosto.objects.all().delete()
        Carrera.objects.all().delete()
        Bodega.objects.all().delete()
        Persona.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Base de datos limpia. Creando datos de ejemplo..."))

        # 1. Carreras
        c_medicina = Carrera.objects.create(nombre="Medicina", codigo="MED-001", coordinador="Dr. Andrés Silva", descripcion="Facultad de Ciencias de la Salud")
        c_enfermeria = Carrera.objects.create(nombre="Enfermería", codigo="ENF-002", coordinador="Lic. Elena Rosales", descripcion="Facultad de Ciencias de la Salud")
        c_software = Carrera.objects.create(nombre="Desarrollo de Software", codigo="SOF-003", coordinador="Ing. Carlos Mendoza", descripcion="PUCE TEC - Tecnologías")

        # 2. Centros de Costo
        cc_bioquimica = CentroCosto.objects.create(carrera=c_medicina, text_id=None, nombre="Laboratorio de Bioquímica", codigo="CC-MED-01", descripcion="Reactivos y análisis clínico") if hasattr(CentroCosto, 'text_id') else CentroCosto.objects.create(carrera=c_medicina, nombre="Laboratorio de Bioquímica", codigo="CC-MED-01", descripcion="Reactivos y análisis clínico")
        cc_simulacion = CentroCosto.objects.create(carrera=c_enfermeria, text_id=None, nombre="Centro de Simulación Clínica", codigo="CC-ENF-02", descripcion="Simuladores y prácticas hospitalarias") if hasattr(CentroCosto, 'text_id') else CentroCosto.objects.create(carrera=c_enfermeria, nombre="Centro de Simulación Clínica", codigo="CC-ENF-02", descripcion="Simuladores y prácticas hospitalarias")
        cc_computo = CentroCosto.objects.create(carrera=c_software, text_id=None, nombre="Laboratorio de Cómputo Avanzado", codigo="CC-SOF-03", descripcion="Servidores, desarrollo y redes") if hasattr(CentroCosto, 'text_id') else CentroCosto.objects.create(carrera=c_software, nombre="Laboratorio de Cómputo Avanzado", codigo="CC-SOF-03", descripcion="Servidores, desarrollo y redes")

        # 3. Bodegas
        b_principal = Bodega.objects.create(nombre="Bodega Central de Insumos", tipo_bodega="910_Vigentes", ubicacion="Edificio Administrativo, Piso 1")
        b_diario = Bodega.objects.create(nombre="Bodega de Uso Diario (Lab)", tipo_bodega="Uso_Diario", ubicacion="Subsuelo de Laboratorios, Aula 102")
        b_limpieza = Bodega.objects.create(nombre="Almacén de Reactivos y Limpieza", tipo_bodega="Limpieza", ubicacion="Exterior, Bloque C")

        # 4. Categorías de Activos Fijos
        ca_equipos = CategoriaActivo.objects.create(nombre="Equipos Médicos e Instrumentación", descripcion="Equipos para prácticas clínicas y de laboratorio")
        ca_tecnologia = CategoriaActivo.objects.create(nombre="Equipos de Computación", descripcion="Servidores, computadoras de escritorio y redes")
        ca_mobiliario = CategoriaActivo.objects.create(nombre="Mobiliario de Laboratorio", descripcion="Mesas de trabajo, vitrinas y estanterías")

        # 5. Activos Fijos
        act_microscopio = ActivoFijo.objects.create(
            carrera=c_medicina,
            centro_costo=cc_bioquimica,
            categoria_activo=ca_equipos,
            codigo_inventario="ACT-MED-1002",
            nombre="Microscopio Binocular LED",
            descripcion="Microscopio marca Olympus para análisis celular avanzado",
            valor_adquisicion=Decimal("1250.00"),
            fecha_adquisicion=timezone.now().date() - timedelta(days=365),
            estado="Operativo",
            ubicacion_actual="Laboratorio de Bioquímica - Vitrina 3"
        )

        act_servidor = ActivoFijo.objects.create(
            carrera=c_software,
            centro_costo=cc_computo,
            categoria_activo=ca_tecnologia,
            codigo_inventario="ACT-SOF-2054",
            nombre="Servidor Dell PowerEdge R740",
            descripcion="Servidor rackeable de base de datos y virtualización",
            valor_adquisicion=Decimal("4500.00"),
            fecha_adquisicion=timezone.now().date() - timedelta(days=200),
            estado="Operativo",
            ubicacion_actual="Sala de Rack 1 - Servidor Principal"
        )

        act_simulador = ActivoFijo.objects.create(
            carrera=c_enfermeria,
            centro_costo=cc_simulacion,
            categoria_activo=ca_equipos,
            codigo_inventario="ACT-ENF-3011",
            nombre="Simulador de Paciente Clínico Adulto",
            descripcion="Maniquí interactivo inteligente para simulación de signos vitales",
            valor_adquisicion=Decimal("8900.00"),
            fecha_adquisicion=timezone.now().date() - timedelta(days=500),
            estado="Necesita Mantenimiento",
            ubicacion_actual="Sala de Simulación 2"
        )

        # 6. Personas (Responsables y Técnicos)
        pers_juan = Persona.objects.create(nombres="Juan Carlos", apellidos="Pérez Díaz", email="j.perez@pucetec.edu.ec", telefono="0998877665", rol="TECNICO")
        pers_maria = Persona.objects.create(nombres="María Belén", apellidos="Cárdenas", email="m.cardenas@pucetec.edu.ec", telefono="0992233445", rol="LABORATORIO")

        # 7. Mantenimientos (uno en próximos 4 días, otro en próximos 6 días)
        Mantenimiento.objects.create(
            activo_fijo=act_microscopio,
            persona=pers_juan,
            tipo="Preventivo",
            fecha_programada=timezone.now().date() + timedelta(days=4),
            descripcion="Limpieza de prismas ópticos y calibración de luz LED",
            estado="Programado"
        )

        Mantenimiento.objects.create(
            activo_fijo=act_simulador,
            persona=pers_juan,
            tipo="Correctivo",
            fecha_programada=timezone.now().date() + timedelta(days=6),
            descripcion="Reparación de módulo de pulso y presión arterial interactivo",
            estado="Programado"
        )

        # 8. Categorías de Insumos
        cat_quimicos = CategoriaInsumo.objects.create(nombre="Reactivos y Químicos", descripcion="Líquidos y solventes de uso delicado")
        cat_descartables = CategoriaInsumo.objects.create(nombre="Material Descartable", descripcion="Insumos de un solo uso de laboratorio")
        cat_instrumentos = CategoriaInsumo.objects.create(nombre="Instrumentación Menor", descripcion="Herramientas y utensilios de laboratorio reusables")

        # 9. Insumos
        ins_alcohol = Insumo.objects.create(categoria_insumo=cat_quimicos, codigo="INS-QUI-101", nombre="Alcohol Etílico 96%", unidad_medida="Litros", es_perecedero=True)
        ins_guantes = Insumo.objects.create(categoria_insumo=cat_descartables, codigo="INS-DES-202", nombre="Guantes de Látex Quirúrgico", unidad_medida="Cajas", es_perecedero=False)
        ins_pipetas = Insumo.objects.create(categoria_insumo=cat_instrumentos, codigo="INS-INS-303", nombre="Pipetas de Pasteur 3ml", unidad_medida="Unidades", es_perecedero=False)
        ins_salina = Insumo.objects.create(categoria_insumo=cat_quimicos, codigo="INS-QUI-104", nombre="Solución Salina Fisiológica 0.9%", unidad_medida="Bolsas", es_perecedero=True)

        # 10. Stock de Insumos (con Alertas de Stock Bajo y Caducidad Próxima)
        # Alcohol Etílico: Stock de 12 (mínimo 5). Caduca en 15 días -> ¡Alerta de Caducidad!
        StockInsumo.objects.create(
            insumo=ins_alcohol,
            bodega=b_principal,
            cantidad_actual=Decimal("12.00"),
            cantidad_minima=Decimal("5.00"),
            lote="LOT-ALC-96",
            fecha_caducidad=timezone.now().date() + timedelta(days=15)
        )

        # Guantes de Látex: Stock de 2 (mínimo 10) -> ¡Alerta de Stock Bajo!
        StockInsumo.objects.create(
            insumo=ins_guantes,
            bodega=b_principal,
            cantidad_actual=Decimal("2.00"),
            cantidad_minima=Decimal("10.00"),
            lote="LOT-GUA-01"
        )

        # Pipetas de Pasteur: Stock normal de 150 (mínimo 15)
        StockInsumo.objects.create(
            insumo=ins_pipetas,
            bodega=b_diario,
            cantidad_actual=Decimal("150.00"),
            cantidad_minima=Decimal("15.00"),
            lote="LOT-PIP-99"
        )

        # Solución Salina: Stock de 4 (mínimo 5). Caduca en 10 días -> ¡Alerta de Stock Bajo Y Caducidad!
        StockInsumo.objects.create(
            insumo=ins_salina,
            bodega=b_diario,
            cantidad_actual=Decimal("4.00"),
            cantidad_minima=Decimal("5.00"),
            lote="LOT-SAL-09",
            fecha_caducidad=timezone.now().date() + timedelta(days=10)
        )

        # 11. Solicitudes de Insumos (con distintos estados para poblar las notificaciones del feed)

        # Solicitud 1: Recibida (Completada)
        sol_1 = Solicitud.objects.create(carrera=c_medicina, centro_costo=cc_bioquimica, persona=pers_maria, estado="Recibida", observacion="Prácticas de bioquímica ciclo 1")
        DetalleSolicitud.objects.create(solicitud=sol_1, insumo=ins_alcohol, cantidad_solicitada=Decimal("4.00"))
        DetalleSolicitud.objects.create(solicitud=sol_1, insumo=ins_pipetas, cantidad_solicitada=Decimal("20.00"))

        # Solicitud 2: Comprada (Esperando recepción de mercadería)
        sol_2 = Solicitud.objects.create(carrera=c_enfermeria, centro_costo=cc_simulacion, persona=pers_maria, estado="Comprada", observacion="Kits de simulación clínica")
        DetalleSolicitud.objects.create(solicitud=sol_2, insumo=ins_guantes, cantidad_solicitada=Decimal("12.00"))

        # Solicitud 3: Aprobada (Lista para registrar compra)
        sol_3 = Solicitud.objects.create(carrera=c_medicina, centro_costo=cc_bioquimica, persona=pers_maria, estado="Aprobada", observacion="Insumos de reserva")
        DetalleSolicitud.objects.create(solicitud=sol_3, insumo=ins_salina, cantidad_solicitada=Decimal("8.00"))

        # Solicitud 4: Pendiente (Nueva solicitud en feed de alerta)
        sol_4 = Solicitud.objects.create(carrera=c_software, centro_costo=cc_computo, persona=pers_maria, estado="Pendiente", observacion="Materiales de limpieza de servidores")
        DetalleSolicitud.objects.create(solicitud=sol_4, insumo=ins_guantes, cantidad_solicitada=Decimal("3.00"))

        # 12. Compras Asociadas

        # Compra para Solicitud 1: Recibida
        compra_1 = Compra.objects.create(
            solicitud=sol_1,
            fecha_compra=timezone.now().date() - timedelta(days=10),
            proveedor="Importadora Médica del Ecuador",
            monto_total=Decimal("185.00"),
            estado="Recibida"
        )

        # Compra para Solicitud 2: Pendiente (Lista para ser recibida por el Bodeguero)
        compra_2 = Compra.objects.create(
            solicitud=sol_2,
            fecha_compra=timezone.now().date() - timedelta(days=1),
            proveedor="Químicos y Equipamiento S.A.",
            monto_total=Decimal("320.00"),
            estado="Pendiente"
        )

        # 13. Historial de movimientos de insumos
        MovimientoInsumo.objects.create(insumo=ins_alcohol, bodega=b_principal, tipo="INGRESO", cantidad=Decimal("12.00"), observacion="Carga inicial de stock", usuario=None)
        MovimientoInsumo.objects.create(insumo=ins_guantes, bodega=b_principal, tipo="INGRESO", cantidad=Decimal("2.00"), observacion="Carga inicial de stock", usuario=None)
        MovimientoInsumo.objects.create(insumo=ins_pipetas, bodega=b_diario, tipo="INGRESO", cantidad=Decimal("150.00"), observacion="Carga inicial de stock", usuario=None)
        MovimientoInsumo.objects.create(insumo=ins_salina, bodega=b_diario, tipo="INGRESO", cantidad=Decimal("4.00"), observacion="Carga inicial de stock", usuario=None)

        self.stdout.write(self.style.SUCCESS("¡Datos de ejemplo cargados exitosamente! Todo listo para la revisión."))
