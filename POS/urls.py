from django.contrib import admin
from django.urls import path, include
from POSNAT import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Principal
    path('admin/', admin.site.urls),
    path('', views.landing, name="landing"),
    #Aplicacion miembros
    path('miembros/', include('miembros.urls')),
    path('miembros/', include('django.contrib.auth.urls')),
    #Ordenes
    path('ordenes/', views.ordenes, name="ordenes"),
    path('orden/nueva/', views.orden_nueva, name="orden_nueva"),
    #
    
    path('menu/', views.menu, name="menu"),
    path('carrito/', views.carrito, name="carrito"),
    path('recetas/', views.recetas, name="recetas"),
    path('clientes/', views.clientes, name="clientes"),
    path('clientes/nuevo', views.clientes_nuevo, name="clientes_nuevo"),
    path('clientes/actualizar/<int:cliente_id>/', views.clientes_actualizar, name='clientes_actualizar'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('inventario/', views.inventario, name="inventario"),
    path('inventario/nuevo', views.inventario_nuevo, name="inventario_nuevo"),
    path('inventario/actualizar/<int:ingrediente_id>/', views.inventario_actualizar, name='inventario_actualizar'),
    path('inventario/eliminar/<int:ingrediente_id>/', views.inventario_eliminar, name='inventario_eliminar'),
    path('tipo/nuevo/', views.tipo_nuevo, name='tipo_nuevo'),
    path('bebidas/', views.bebidas, name='bebidas'),
    path('bebida/nueva/', views.bebida_nueva, name='bebida_nueva'),
    path('bebida/actualizar/<int:bebida_id>/', views.bebida_actualizar, name='bebida_actualizar'),
    path('bebida/eliminar/<int:bebida_id>/', views.bebida_eliminar, name='bebida_eliminar'),
    path('categoria/nueva/', views.categoria_nueva, name='categoria_nueva'),
    path('proveedores/', views.proveedores, name="proveedores"),
    path('proveedores/nuevo', views.proveedores_nuevo, name="proveedores_nuevo"),
    path('proveedores/actualizar/<int:proveedor_id>/', views.proveedores_actualizar, name='proveedores_actualizar'),
    path('proveedores/eliminar/<int:proveedor_id>/', views.proveedores_eliminar, name='proveedores_eliminar'),
    path('prueba/', views.prueba, name="prueba"),
    path('bebida/<int:bebida_id>/ingredientes/', views.obtener_ingredientes, name='obtener_ingredientes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
