from django.contrib import admin
from .models import (
    Proveedor,
    Categoria,
    Tipo,
    Ingrediente,
    Bebida,
    Venta,
    Cliente,
    DetalleVenta,
    ReporteVenta,
)

admin.site.register(Proveedor)
admin.site.register(Categoria)
admin.site.register(Tipo)
admin.site.register(Ingrediente)
admin.site.register(Bebida)
admin.site.register(Venta)
admin.site.register(Cliente)
admin.site.register(DetalleVenta)
admin.site.register(ReporteVenta)
