from django.urls import path

from . import views


app_name = 'transport_app'

urlpatterns = [
    path('inicio/', views.bienvenida, name='bienvenida'),
]