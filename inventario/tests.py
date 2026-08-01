from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from .models import (
    Carrera, CentroCosto, Bodega, CategoriaInsumo, Insumo, StockInsumo, MovimientoInsumo,
    Persona, Solicitud, DetalleSolicitud, Compra
)
from .forms import MovimientoInsumoForm

User = get_user_model()

class Sprint2Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin_test',
            password='password123',
            email='admin@test.com'
        )
        self.carrera = Carrera.objects.create(
            nombre="Medicina",
            codigo="MED001"
        )
        self.client.login(username='admin_test', password='password123')

    def test_carrera_creation(self):
        response = self.client.post(reverse('carrera_create'), {
            'nombre': 'Enfermería',
            'codigo': 'ENF001',
            'activo': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Carrera.objects.filter(nombre='Enfermería').exists())

    def test_centro_costo_creation(self):
        response = self.client.post(reverse('centro_costo_create'), {
            'carrera': self.carrera.id,
            'nombre': 'Laboratorio Clínico',
            'codigo': 'LAB001',
            'activo': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CentroCosto.objects.filter(nombre='Laboratorio Clínico').exists())

    def test_bodega_creation(self):
        response = self.client.post(reverse('bodega_create'), {
            'nombre': 'Bodega Central',
            'tipo_bodega': '910_Vigentes',
            'activo': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Bodega.objects.filter(nombre='Bodega Central').exists())

    def test_lists_load(self):
        urls = ['carrera_list', 'centro_costo_list', 'bodega_list']
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)


class Sprint4Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin_test',
            password='password123',
            email='admin@test.com'
        )
        self.client.login(username='admin_test', password='password123')

        self.bodega = Bodega.objects.create(
            nombre="Bodega de Pruebas",
            tipo_bodega="Uso_Diario"
        )
        self.categoria = CategoriaInsumo.objects.create(
            nombre="Químicos",
            descripcion="Reactivos químicos y solventes"
        )
        self.insumo = Insumo.objects.create(
            categoria_insumo=self.categoria,
            codigo="CHEM001",
            nombre="Alcohol Etílico 96%",
            unidad_medida="Litros",
            es_perecedero=True
        )

    def test_categoria_insumo_creation(self):
        response = self.client.post(reverse('categoria_insumo_create'), {
            'nombre': 'Vidriería',
            'descripcion': 'Material de vidrio de laboratorio'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CategoriaInsumo.objects.filter(nombre='Vidriería').exists())

    def test_insumo_creation(self):
        response = self.client.post(reverse('insumo_create'), {
            'categoria_insumo': self.categoria.id,
            'codigo': 'CHEM002',
            'nombre': 'Agua Destilada',
            'unidad_medida': 'Galones',
            'es_perecedero': False,
            'activo': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Insumo.objects.filter(nombre='Agua Destilada').exists())

    def test_stock_insumo_creation(self):
        response = self.client.post(reverse('stock_insumo_create'), {
            'insumo': self.insumo.id,
            'bodega': self.bodega.id,
            'cantidad_actual': 10,
            'cantidad_minima': 2,
            'lote': 'L-101',
            'fecha_caducidad': '2026-12-31'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(StockInsumo.objects.filter(insumo=self.insumo, bodega=self.bodega).exists())

    def test_movimiento_insumo_ingreso(self):
        response = self.client.post(reverse('movimiento_insumo_create'), {
            'insumo': self.insumo.id,
            'bodega': self.bodega.id,
            'tipo': 'INGRESO',
            'cantidad': 15.5,
            'observacion': 'Compra inicial'
        })
        self.assertEqual(response.status_code, 302)
        stock = StockInsumo.objects.get(insumo=self.insumo, bodega=self.bodega)
        self.assertEqual(stock.cantidad_actual, 15.5)

    def test_movimiento_insumo_egreso_valid(self):
        StockInsumo.objects.create(
            insumo=self.insumo,
            bodega=self.bodega,
            cantidad_actual=20.0,
            cantidad_minima=5.0
        )
        response = self.client.post(reverse('movimiento_insumo_create'), {
            'insumo': self.insumo.id,
            'bodega': self.bodega.id,
            'tipo': 'EGRESO',
            'cantidad': 5.0,
            'observacion': 'Consumo diario'
        })
        self.assertEqual(response.status_code, 302)
        stock = StockInsumo.objects.get(insumo=self.insumo, bodega=self.bodega)
        self.assertEqual(stock.cantidad_actual, 15.0)

    def test_movimiento_insumo_egreso_insufficient_stock(self):
        StockInsumo.objects.create(
            insumo=self.insumo,
            bodega=self.bodega,
            cantidad_actual=3.0,
            cantidad_minima=1.0
        )
        form_data = {
            'insumo': self.insumo,
            'bodega': self.bodega,
            'tipo': 'EGRESO',
            'cantidad': 5.0,
            'observacion': 'Intentando sacar de más'
        }
        form = MovimientoInsumoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Stock insuficiente', form.errors['__all__'][0])

    def test_lists_and_alerts_load(self):
        urls = ['categoria_insumo_list', 'insumo_list', 'stock_insumo_list', 'movimiento_insumo_list', 'dashboard_alertas']
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)


class Sprint5Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin_test',
            password='password123',
            email='admin@test.com'
        )
        self.client.login(username='admin_test', password='password123')

        self.carrera = Carrera.objects.create(nombre="Medicina", codigo="MED001")
        self.centro_costo = CentroCosto.objects.create(carrera=self.carrera, nombre="Lab Química", codigo="LQ01")
        self.persona = Persona.objects.create(nombres="Juan", apellidos="Pérez", rol="TECNICO")
        self.bodega = Bodega.objects.create(nombre="Bodega Insumos", tipo_bodega="Uso_Diario")

        self.categoria = CategoriaInsumo.objects.create(nombre="Reactivos")
        self.insumo = Insumo.objects.create(
            categoria_insumo=self.categoria,
            codigo="INS-101",
            nombre="Pipetas de Pasteur",
            unidad_medida="Unidades"
        )

    def test_solicitud_creation_and_details_rendering(self):
        # Create a Solicitud and inline DetalleSolicitud using the view
        data = {
            'carrera': self.carrera.id,
            'centro_costo': self.centro_costo.id,
            'persona': self.persona.id,
            'observacion': 'Solicitud urgente para el laboratorio',
            # inline formset data (DetalleSolicitudFormSet)
            'detalles-TOTAL_FORMS': '1',
            'detalles-INITIAL_FORMS': '0',
            'detalles-MIN_NUM_FORMS': '0',
            'detalles-MAX_NUM_FORMS': '1000',
            'detalles-0-insumo': self.insumo.id,
            'detalles-0-cantidad_solicitada': '50',
            'detalles-0-id': '',
        }
        response = self.client.post(reverse('solicitud_create'), data)
        self.assertEqual(response.status_code, 302)

        # Verify Solicitud and DetalleSolicitud exist
        solicitud = Solicitud.objects.get(observacion='Solicitud urgente para el laboratorio')
        self.assertEqual(solicitud.estado, 'Pendiente')
        self.assertEqual(solicitud.detalles.count(), 1)
        self.assertEqual(solicitud.detalles.first().cantidad_solicitada, 50)

        # Verify Detail page loads
        response = self.client.get(reverse('solicitud_detail', kwargs={'pk': solicitud.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pipetas de Pasteur')

    def test_solicitud_approval_and_rejection_flows(self):
        sol = Solicitud.objects.create(
            carrera=self.carrera,
            centro_costo=self.centro_costo,
            persona=self.persona,
            observacion='Flujo aprobación'
        )

        # 1. Approve
        response = self.client.get(reverse('solicitud_approve', kwargs={'pk': sol.id}))
        self.assertEqual(response.status_code, 302)
        sol.refresh_from_db()
        self.assertEqual(sol.estado, 'Aprobada')

        # 2. Reject
        response = self.client.get(reverse('solicitud_reject', kwargs={'pk': sol.id}))
        self.assertEqual(response.status_code, 302)
        sol.refresh_from_db()
        self.assertEqual(sol.estado, 'Rechazada')

    def test_compra_creation_from_solicitud(self):
        sol = Solicitud.objects.create(
            carrera=self.carrera,
            centro_costo=self.centro_costo,
            persona=self.persona,
            estado='Aprobada'
        )

        # Create Compra linked to Solicitud
        response = self.client.post(reverse('compra_create'), {
            'solicitud': sol.id,
            'fecha_compra': '2025-05-15',
            'proveedor': 'Distribuidora Científica',
            'monto_total': 345.50,
            'estado': 'Pendiente'
        })
        self.assertEqual(response.status_code, 302)

        # Verify purchase and request status updated to 'Comprada'
        compra = Compra.objects.get(proveedor='Distribuidora Científica')
        self.assertEqual(compra.solicitud, sol)

        sol.refresh_from_db()
        self.assertEqual(sol.estado, 'Comprada')

    def test_compra_merchandise_reception_intake(self):
        sol = Solicitud.objects.create(
            carrera=self.carrera,
            centro_costo=self.centro_costo,
            persona=self.persona,
            estado='Comprada'
        )
        DetalleSolicitud.objects.create(
            solicitud=sol,
            insumo=self.insumo,
            cantidad_solicitada=120
        )
        compra = Compra.objects.create(
            solicitud=sol,
            fecha_compra='2025-05-15',
            proveedor='Distribuidora Científica',
            monto_total=1200.00,
            estado='Pendiente'
        )

        # Receive merchandise in the Bodega
        response = self.client.post(reverse('compra_recibir', kwargs={'pk': compra.id}), {
            'bodega': self.bodega.id
        })
        self.assertEqual(response.status_code, 302)

        # Check states updated to 'Recibida'
        compra.refresh_from_db()
        sol.refresh_from_db()
        self.assertEqual(compra.estado, 'Recibida')
        self.assertEqual(sol.estado, 'Recibida')

        # Verify MovimientoInsumo (INGRESO) registered
        mov = MovimientoInsumo.objects.get(insumo=self.insumo, bodega=self.bodega)
        self.assertEqual(mov.tipo, 'INGRESO')
        self.assertEqual(mov.cantidad, 120)

        # Verify stock updated
        stock = StockInsumo.objects.get(insumo=self.insumo, bodega=self.bodega)
        self.assertEqual(stock.cantidad_actual, 120)

    def test_lists_load(self):
        urls = ['solicitud_list', 'compra_list']
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)
