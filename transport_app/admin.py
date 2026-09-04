from django.contrib import admin

from .models import Conductor, Operador, Ruta, Viaje


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'origen', 'destino', 'distancia_km', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'origen', 'destino')


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'licencia', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'licencia')


@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'correo')


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('ruta', 'conductor', 'operador', 'salida', 'llegada', 'estado')
    list_filter = ('estado', 'salida')
    search_fields = ('ruta__nombre', 'conductor__nombre', 'operador__nombre')
