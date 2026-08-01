from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from .models import Carrera, CentroCosto, Bodega, CategoriaInsumo, Insumo, StockInsumo, MovimientoInsumo
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
        # INGRESO should create/increase StockInsumo
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
        # Create initial stock
        StockInsumo.objects.create(
            insumo=self.insumo,
            bodega=self.bodega,
            cantidad_actual=20.0,
            cantidad_minima=5.0
        )
        # EGRESO within limits should succeed and decrease stock
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
        # Create initial stock of 3.0
        StockInsumo.objects.create(
            insumo=self.insumo,
            bodega=self.bodega,
            cantidad_actual=3.0,
            cantidad_minima=1.0
        )
        # EGRESO of 5.0 should fail form validation (insufficient stock)
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
