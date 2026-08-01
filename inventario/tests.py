from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Carrera, CentroCosto, Bodega

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
