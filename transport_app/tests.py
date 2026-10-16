from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Conductor, Operador, Ruta, Viaje


class ApiCrudTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ruta = Ruta.objects.create(
            nombre='Centro - Aeropuerto',
            origen='Centro',
            destino='Aeropuerto',
            distancia_km='25.50',
        )
        cls.conductor = Conductor.objects.create(
            nombre='Ana Pérez',
            licencia='LIC-100',
        )
        cls.operador = Operador.objects.create(
            nombre='Operador Central',
            correo='central@example.com',
        )

    def test_pagina_404_personalizada(self):
        response = self.client.get('/ruta-inexistente/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertContains(response, 'Ruta no encontrada', status_code=404)

    def test_router_muestra_los_cuatro_recursos(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data),
            {'rutas', 'conductores', 'operadores', 'viajes'},
        )

    def assert_resource_crud(self, basename, payload, replacement, patch):
        collection_url = reverse(f'transport_app:{basename}-list')
        self.assertEqual(
            self.client.get(collection_url).status_code,
            status.HTTP_200_OK,
        )
        response = self.client.post(collection_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        detail_url = reverse(
            f'transport_app:{basename}-detail',
            args=[response.data['id']],
        )
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.client.put(detail_url, replacement, format='json').status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.patch(detail_url, patch, format='json').status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.delete(detail_url).status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            self.client.get(detail_url).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_ruta_conductor_y_operador_crud(self):
        resources = (
            (
                'ruta',
                {
                    'nombre': 'Ruta de prueba',
                    'origen': 'Temuco',
                    'destino': 'Valdivia',
                    'distancia_km': '120.00',
                },
                {
                    'nombre': 'Ruta actualizada',
                    'origen': 'Temuco',
                    'destino': 'Valdivia',
                    'distancia_km': '121.00',
                    'activa': False,
                },
                {'nombre': 'Ruta parcial'},
            ),
            (
                'conductor',
                {
                    'nombre': 'Juan Soto',
                    'licencia': 'LIC-200',
                    'telefono': '912345678',
                },
                {
                    'nombre': 'Juan Soto actualizado',
                    'licencia': 'LIC-201',
                    'telefono': '912345678',
                    'activo': False,
                },
                {'nombre': 'Juan Soto editado'},
            ),
            (
                'operador',
                {
                    'nombre': 'Operador Sur',
                    'correo': 'sur@example.com',
                    'telefono': '987654321',
                },
                {
                    'nombre': 'Operador Sur actualizado',
                    'correo': 'sur-actualizado@example.com',
                    'telefono': '987654321',
                    'activo': False,
                },
                {'nombre': 'Operador Sur editado'},
            ),
        )
        for basename, payload, replacement, patch in resources:
            with self.subTest(resource=basename):
                self.assert_resource_crud(
                    basename,
                    payload,
                    replacement,
                    patch,
                )

    def test_viaje_crud(self):
        self.assert_resource_crud(
            'viaje',
            {
                'ruta': self.ruta.pk,
                'conductor': self.conductor.pk,
                'operador': self.operador.pk,
                'salida': '2026-10-16T09:00:00-03:00',
            },
            {
                'ruta': self.ruta.pk,
                'conductor': self.conductor.pk,
                'operador': self.operador.pk,
                'salida': '2026-10-16T10:00:00-03:00',
                'llegada': None,
                'estado': Viaje.Estado.EN_CURSO,
            },
            {'estado': Viaje.Estado.CANCELADO},
        )

    def test_viaje_rechaza_llegada_anterior_a_salida(self):
        response = self.client.post(
            reverse('transport_app:viaje-list'),
            {
                'ruta': self.ruta.pk,
                'conductor': self.conductor.pk,
                'operador': self.operador.pk,
                'salida': '2026-10-16T10:00:00-03:00',
                'llegada': '2026-10-16T09:00:00-03:00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('llegada', response.data)

    def test_no_permite_eliminar_recursos_con_viajes_asociados(self):
        viaje = Viaje.objects.create(
            ruta=self.ruta,
            conductor=self.conductor,
            operador=self.operador,
            salida='2026-10-16T09:00:00-03:00',
        )
        self.assertIsNotNone(viaje.pk)

        for basename, instance in (
            ('ruta', self.ruta),
            ('conductor', self.conductor),
            ('operador', self.operador),
        ):
            with self.subTest(resource=basename):
                response = self.client.delete(
                    reverse(
                        f'transport_app:{basename}-detail',
                        args=[instance.pk],
                    )
                )
                self.assertEqual(
                    response.status_code,
                    status.HTTP_409_CONFLICT,
                    response.data,
                )
