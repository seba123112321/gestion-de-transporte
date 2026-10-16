from django.db.models.deletion import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Conductor, Operador, Ruta, Viaje
from .serializers import (
    ConductorSerializer,
    OperadorSerializer,
    RutaSerializer,
    ViajeSerializer,
)


class ProtectedDeleteModelViewSet(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response(
                {'detail': 'No se puede eliminar porque hay viajes asociados.'},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class RutaViewSet(ProtectedDeleteModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer


class ConductorViewSet(ProtectedDeleteModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer


class OperadorViewSet(ProtectedDeleteModelViewSet):
    queryset = Operador.objects.all()
    serializer_class = OperadorSerializer


class ViajeViewSet(ProtectedDeleteModelViewSet):
    queryset = Viaje.objects.select_related('ruta', 'conductor', 'operador')
    serializer_class = ViajeSerializer
