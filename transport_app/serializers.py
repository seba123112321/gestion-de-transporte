from rest_framework import serializers

from .models import Conductor, Operador, Ruta, Viaje


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'
        read_only_fields = ('id', 'creado_en', 'actualizado_en')


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'
        read_only_fields = ('id', 'creado_en', 'actualizado_en')


class OperadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operador
        fields = '__all__'
        read_only_fields = ('id', 'creado_en', 'actualizado_en')


class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viaje
        fields = '__all__'
        read_only_fields = ('id', 'creado_en', 'actualizado_en')

    def validate(self, attrs):
        salida = attrs.get('salida', getattr(self.instance, 'salida', None))
        llegada = attrs.get('llegada', getattr(self.instance, 'llegada', None))
        if salida and llegada and llegada <= salida:
            raise serializers.ValidationError({
                'llegada': 'La llegada debe ser posterior a la salida.',
            })
        return attrs
