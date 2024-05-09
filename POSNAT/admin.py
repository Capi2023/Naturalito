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
    DetalleVentaIngrediente,
    TamañoBebida  # Asegúrate de incluir TamañoBebida si no lo has hecho ya
)

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'compañía', 'correo', 'numero')
    search_fields = ('nombre', 'compañía', 'correo', 'numero')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

class TipoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio_extra', 'cantidad_disponible', 'unidad')
    search_fields = ('nombre', 'tipo__nombre')
    list_filter = ('tipo', 'unidad')

class BebidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'disponible')
    search_fields = ('nombre', 'categoria__nombre')
    list_filter = ('categoria', 'disponible')
    filter_horizontal = ('ingredientes', 'tamaños')  # Añadir 'tamaños' si estás utilizando la relación ManyToMany

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'correo', 'puntos')
    search_fields = ('nombre', 'apellido', 'telefono', 'correo')

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

class VentaAdmin(admin.ModelAdmin):
    list_display = ('fecha_venta', 'cliente', 'total', 'estado')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'estado')
    list_filter = ('fecha_venta', 'estado')
    inlines = [DetalleVentaInline]

class ReporteVentaAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'tipo_periodo', 'total_ventas', 'total_bebidas_vendidas', 'cantidad_de_clientes')
    search_fields = ('tipo_periodo',)
    list_filter = ('tipo_periodo', 'fecha_inicio')

class DetalleVentaIngredienteAdmin(admin.ModelAdmin):
    list_display = ('detalle_venta', 'ingrediente', 'cantidad')
    search_fields = ('detalle_venta__venta__id', 'ingrediente__nombre')

class TamañoBebidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_agua', 'cantidad_leche')
    search_fields = ('nombre',)

admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)
admin.site.register(Bebida, BebidaAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(DetalleVenta)
admin.site.register(ReporteVenta, ReporteVentaAdmin)
admin.site.register(DetalleVentaIngrediente, DetalleVentaIngredienteAdmin)
admin.site.register(TamañoBebida, TamañoBebidaAdmin)

