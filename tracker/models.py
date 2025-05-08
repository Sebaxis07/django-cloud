from django.db import models
from django.utils import timezone
from decimal import Decimal

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class Transaccion(models.Model):
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='transacciones')
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.descripcion} - ${self.monto} ({self.fecha.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-fecha', '-id']
        verbose_name_plural = "Transacciones"