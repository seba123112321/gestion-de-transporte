from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views, views


app_name = 'transport_app'

router = DefaultRouter()
router.register('rutas', api_views.RutaViewSet, basename='ruta')
router.register('conductores', api_views.ConductorViewSet, basename='conductor')
router.register('operadores', api_views.OperadorViewSet, basename='operador')
router.register('viajes', api_views.ViajeViewSet, basename='viaje')

urlpatterns = [
    path('inicio/', views.bienvenida, name='bienvenida'),
    path('api/', include(router.urls)),
]