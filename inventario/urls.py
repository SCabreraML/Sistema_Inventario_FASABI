from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Carreras
    path('carreras/', views.CarreraListView.as_view(), name='carrera_list'),
    path('carreras/nuevo/', views.CarreraCreateView.as_view(), name='carrera_create'),
    path('carreras/editar/<int:pk>/', views.CarreraUpdateView.as_view(), name='carrera_update'),

    # Centros de Costo
    path('centros-costo/', views.CentroCostoListView.as_view(), name='centro_costo_list'),
    path('centros-costo/nuevo/', views.CentroCostoCreateView.as_view(), name='centro_costo_create'),
    path('centros-costo/editar/<int:pk>/', views.CentroCostoUpdateView.as_view(), name='centro_costo_update'),

    # Bodegas
    path('bodegas/', views.BodegaListView.as_view(), name='bodega_list'),
    path('bodegas/nuevo/', views.BodegaCreateView.as_view(), name='bodega_create'),
    path('bodegas/editar/<int:pk>/', views.BodegaUpdateView.as_view(), name='bodega_update'),

    # Activos Fijos
    path('activos/', views.ActivoFijoListView.as_view(), name='activo_list'),
    path('activos/nuevo/', views.ActivoFijoCreateView.as_view(), name='activo_create'),
    path('activos/editar/<int:pk>/', views.ActivoFijoUpdateView.as_view(), name='activo_update'),

    # Categorias Activos
    path('activos/categorias/', views.CategoriaActivoListView.as_view(), name='categoria_activo_list'),
    path('activos/categorias/nuevo/', views.CategoriaActivoCreateView.as_view(), name='categoria_activo_create'),

    # Mantenimientos
    path('mantenimientos/', views.MantenimientoListView.as_view(), name='mantenimiento_list'),
    path('mantenimientos/nuevo/', views.MantenimientoCreateView.as_view(), name='mantenimiento_create'),

    # Historial Activos
    path('activos/historial/', views.MovimientoActivoListView.as_view(), name='movimiento_activo_list'),

    # Reportes y Alertas
    path('reportes/activos/', views.reportes_activos, name='reporte_activos'),
    path('dashboard/alertas/', views.dashboard_alertas, name='dashboard_alertas'),

    # --- SPRINT 4 URLS ---

    # Categorias Insumos
    path('insumos/categorias/', views.CategoriaInsumoListView.as_view(), name='categoria_insumo_list'),
    path('insumos/categorias/nuevo/', views.CategoriaInsumoCreateView.as_view(), name='categoria_insumo_create'),
    path('insumos/categorias/editar/<int:pk>/', views.CategoriaInsumoUpdateView.as_view(), name='categoria_insumo_update'),

    # Insumos
    path('insumos/', views.InsumoListView.as_view(), name='insumo_list'),
    path('insumos/nuevo/', views.InsumoCreateView.as_view(), name='insumo_create'),
    path('insumos/editar/<int:pk>/', views.InsumoUpdateView.as_view(), name='insumo_update'),

    # Stock Insumos
    path('insumos/stock/', views.StockInsumoListView.as_view(), name='stock_insumo_list'),
    path('insumos/stock/nuevo/', views.StockInsumoCreateView.as_view(), name='stock_insumo_create'),
    path('insumos/stock/editar/<int:pk>/', views.StockInsumoUpdateView.as_view(), name='stock_insumo_update'),

    # Movimientos Insumos
    path('insumos/movimientos/', views.MovimientoInsumoListView.as_view(), name='movimiento_insumo_list'),
    path('insumos/movimientos/nuevo/', views.MovimientoInsumoCreateView.as_view(), name='movimiento_insumo_create'),
]
