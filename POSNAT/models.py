from django.db import models
from django.utils import timezone


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    compañía = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()
    numero = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.compañía}"


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
    UNIDADES = [
        ('gramos', 'Gramos'),
        ('onzas', 'Onzas'),
    ]

    UNIDADES_ORIGINALES = [
        ('litros', 'Litros'),
        ('kilogramos', 'Kilogramos'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='ingredientes/', default='static/images/sin.jpg')
    precio_extra = models.DecimalField(max_digits=5, decimal_places=2)
    cantidad_porcion_extra = models.PositiveIntegerField(default=0)
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Se usa DecimalField para mayor precisión
    cantidad_minima = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad_original = models.CharField(max_length=10, choices=UNIDADES_ORIGINALES, default='kilogramos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    detalles = models.TextField(blank=True, null=True)
    unidad = models.CharField(max_length=10, choices=UNIDADES, default='gramos')

    def __str__(self):
        return self.nombre


class TamañoBebida(models.Model):
    TAMAÑOS = [
        ('chico', 'Chico'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]

    nombre = models.CharField(max_length=50, choices=TAMAÑOS, unique=True)
    cantidad_agua = models.PositiveIntegerField()
    cantidad_leche = models.PositiveIntegerField()

    def __str__(self):
        return self.get_nombre_display()


class Bebida(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='bebidas/', default='static/images/sin.jpg')
    ingredientes = models.ManyToManyField(Ingrediente)
    precio_base = models.DecimalField(max_digits=8, decimal_places=2)
    detalles = models.TextField(blank=True, null=True)
    disponible = models.BooleanField(default=True)
    tamaños = models.ManyToManyField(TamañoBebida)

    def __str__(self):
        return self.nombre



class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    puntos = models.IntegerField(default=0)

    def añadir_puntos(self, puntos):
        self.puntos += puntos
        self.save()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Puntos: {self.puntos}"


class Venta(models.Model):
    fecha_venta = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    detalles = models.TextField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, default='pendiente')

    def calcular_total(self):
        total = 0
        for detalle_venta in self.detalleventa_set.all():
            total += detalle_venta.subtotal()
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta del {self.fecha_venta.strftime('%Y-%m-%d %H:%M')} - Total: {self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    ingredientes_extra = models.ManyToManyField(Ingrediente, through='DetalleVentaIngrediente')
    comentarios = models.TextField(blank=True, null=True)

    def subtotal(self):
        total_base = self.cantidad * self.precio_unitario
        total_ingredientes = 0
        for ingrediente in self.detalleventaingrediente_set.all():
            total_ingredientes += ingrediente.cantidad * ingrediente.ingrediente.precio_extra
        return total_base + total_ingredientes

    def __str__(self):
        return f'Detalle de Venta - {self.venta} - Producto: {self.bebida.nombre} - Cantidad: {self.cantidad}'


class DetalleVentaIngrediente(models.Model):
    detalle_venta = models.ForeignKey(DetalleVenta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.cantidad}x {self.ingrediente.nombre} para {self.detalle_venta}'


class ReporteVenta(models.Model):
    TIPOS_DE_PERIODO = [
        ('Dia', 'Día'),
        ('Semana', 'Semana'),
        ('Mes', 'Mes'),
    ]
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    tipo_periodo = models.CharField(max_length=10, choices=TIPOS_DE_PERIODO)
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2)
    total_bebidas_vendidas = models.PositiveIntegerField(default=0)
    cantidad_de_clientes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Reporte de Ventas - {self.tipo_periodo} {self.fecha_inicio}"

