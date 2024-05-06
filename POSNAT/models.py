from django.db import models
from django.utils import timezone
from abc import ABC, abstractmethod


class BebidaDecorator(ABC):
    def __init__(self, bebida):
        self.bebida = bebida

    @abstractmethod
    def precio_total(self):
        pass


class BebidaDecorada(BebidaDecorator):
    def __init__(self, bebida, ingredientes_decoradores):
        super().__init__(bebida)
        self.ingredientes_decoradores = ingredientes_decoradores

    def precio_total(self):
        precio_total = self.bebida.precio_base
        for ingrediente in self.ingredientes_decoradores.all():
            precio_total += ingrediente.precio_extra
        return precio_total


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    compañia = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()
    numero = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.compañia}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Tipo(models.Model):
    nombre = models.CharField(max_length=100)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='ingrediente/', default='static\images\sin.jpg')
    precio_extra = models.DecimalField(max_digits=5, decimal_places=2)
    cantidad_extra = models.PositiveIntegerField(default=0)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    cantidad_minima = models.PositiveIntegerField(default=10)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Bebida(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='bebidas/', default='static\images\sin.jpg')
    ingredientes = models.ManyToManyField(Ingrediente)
    precio_base = models.DecimalField(max_digits=8, decimal_places=2)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Venta(models.Model):    
    fecha_venta = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    detalles = models.TextField(blank=True, null=True)
    bebida = models.ManyToManyField(Bebida, through='DetalleVenta')

    def calcular_total(self):
        total = 0
        for detalle_venta in self.detalleventa_set.all():
            total += detalle_venta.subtotal()
        return total

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    puntos = models.IntegerField(default=0)
    venta = models.ForeignKey(Venta, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Puntos: {self.puntos}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'Detalle de venta - {self.venta} - Producto: {self.bebida.nombre} - Cantidad: {self.cantidad}'


class ReporteVenta(models.Model):
    TIPOS_DE_PERIODO = [
        ('Dia', 'Día'),
        ('Semana', 'Semana'),
        ('Mes', 'Mes'),
    ]
    
    fecha_inicio = models.DateField()
    tipo_periodo = models.CharField(max_length=10, choices=TIPOS_DE_PERIODO)
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reporte de Ventas - {self.tipo_periodo} {self.fecha_inicio}"

