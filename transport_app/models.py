from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


class Ruta(models.Model):
    nombre = models.CharField(max_length=120)
    origen = models.CharField(max_length=120)
    destino = models.CharField(max_length=120)
    distancia_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('origen', 'destino')
        verbose_name = 'ruta'
        verbose_name_plural = 'rutas'

    def __str__(self):
        return f'{self.origen} - {self.destino}'


class Conductor(models.Model):
    nombre = models.CharField(max_length=120)
    licencia = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'conductor'
        verbose_name_plural = 'conductores'

    def __str__(self):
        return self.nombre


class Operador(models.Model):
    nombre = models.CharField(max_length=120)
    correo = models.EmailField(blank=True, null=True, unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'operador'
        verbose_name_plural = 'operadores'

    def __str__(self):
        return self.nombre


class Viaje(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADO = 'programado', 'Programado'
        EN_CURSO = 'en_curso', 'En curso'
        COMPLETADO = 'completado', 'Completado'
        CANCELADO = 'cancelado', 'Cancelado'

    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.PROTECT,
        related_name='viajes',
    )
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.PROTECT,
        related_name='viajes',
    )
    operador = models.ForeignKey(
        Operador,
        on_delete=models.PROTECT,
        related_name='viajes',
    )
    salida = models.DateTimeField()
    llegada = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.PROGRAMADO,
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('salida',)
        verbose_name = 'viaje'
        verbose_name_plural = 'viajes'
        constraints = [
            models.CheckConstraint(
                condition=Q(llegada__isnull=True) | Q(llegada__gt=F('salida')),
                name='viaje_llegada_posterior_a_salida',
            ),
        ]

    def __str__(self):
        return f'{self.ruta} ({self.salida:%Y-%m-%d %H:%M})'
