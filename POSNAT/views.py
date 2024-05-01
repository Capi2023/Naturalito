from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .models import *
from .decorators import *
from .forms import *


def prueba(request):
    return render(request, "home/prueba.html", {})


def landing(request):
    return render(request, "home/landing_page.html", {})


def ordenes(request):
    return render(request, "home/Ordenes.html", {})


def menu(request):
    return render(request, "home/Menu.html", {})


def carrito(request):
    return render(request, "home/Carrito.html", {})


def recetas(request):
    return render(request, "home/Recetas.html", {})


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "home/Clientes.html", {'clientes':clientes})


def clientes_nuevo(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
        else:
            messages.success(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ClienteForm()
    return render(request, 'home/cliente_nuevo.html', {'form': form})


def clientes_actualizar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'home/cliente_actualizar.html', {'form': form, 'cliente_id': cliente_id})


def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes')


def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, "home/Proveedores.html", {'proveedores': proveedores})


def proveedores_nuevo(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('proveedores')

    else:
        form = ProveedorForm()

    return render(request, "home/Proveedor_nuevo.html", {'form': form})


def proveedores_actualizar(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'home/proveedores_actualizar.html', {'form': form, 'proveedor_id': proveedor_id})


def proveedores_eliminar(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.delete()
    return redirect('proveedores')


def inventario(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, "home/Inventario.html", {'ingredientes': ingredientes})


def inventario_nuevo(request):
    tipos = Tipo.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        form = IngredienteForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('inventario')

    else:
        form = IngredienteForm()

    return render(request, 'home/inventario_nuevo.html', {'form': form, 'tipos': tipos, 'proveedores': proveedores})


def inventario_actualizar(request, ingrediente_id):
    tipos = Tipo.objects.all()
    proveedores = Proveedor.objects.all()
    
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)

    if request.method == 'POST':
        form = IngredienteForm(request.POST, request.FILES, instance=ingrediente)
        if form.is_valid():
            cantidad_a_anadir = request.POST.get('cantidad_a_anadir', 0)
            cantidad_disponible_actual = ingrediente.cantidad_disponible
            cantidad_disponible_nueva = cantidad_disponible_actual + int(cantidad_a_anadir)
            form.save()
            ingrediente.cantidad_disponible = cantidad_disponible_nueva
            ingrediente.save()
            return redirect('inventario')
    else:
        form = IngredienteForm(instance=ingrediente)

    return render(request, 'home/Inventario_actualizar.html', {'form': form, 'ingrediente_id': ingrediente.id, 'tipos': tipos, 'proveedores': proveedores})


@agregar_ingrediente
def agregar_ingrediente_a_bebida(request, bebida_id, ingrediente_id, cantidad):
    bebida = get_object_or_404(Bebida, pk=bebida_id)
    ingrediente = get_object_or_404(Ingrediente, pk=ingrediente_id)
    bebida.precio += ingrediente.precio * cantidad
    bebida.save()
    
    # Crear y guardar el detalle de venta
    detalle_venta = DetalleVenta(
        venta=None,  # Esto se llenará en la vista que procesa la venta completa
        bebida=bebida,
        cantidad=cantidad,
        precio_unitario=bebida.precio
    )
    detalle_venta.save()
    
    return render(request, "home/Orden_nueva.html", {'mensaje': f"{cantidad} oz de {ingrediente.nombre} agregados a {bebida.nombre}"})


def inventario_eliminar(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    ingrediente.delete()
    return redirect('inventario')


def tipo_nuevo(request):
    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = TipoForm()
    return render(request, 'home/Tipo_nuevo.html', {'form': form})


def bebidas(request):
    bebidas = Bebida.objects.all()
    return render(request, 'home/bebidas.html', {'bebidas': bebidas})


def bebida_nueva(request):
    if request.method == 'POST':
        form = BebidaForm(request.POST, request.FILES)
        if form.is_valid():
            bebida = form.save(commit=False)
            bebida.save()
            form.save_m2m()
            return redirect('bebidas')
    else:
        form = BebidaForm()
    
    ingredientes = Ingrediente.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'home/bebida_nueva.html', {'form': form, 'ingredientes': ingredientes, 'categorias': categorias})


def bebida_actualizar(request, bebida_id):
    bebida = get_object_or_404(Bebida, id=bebida_id)
    categorias = Categoria.objects.all()
    ingredientes = Ingrediente.objects.all()
    
    if request.method == 'POST':
        form = BebidaForm(request.POST, request.FILES, instance=bebida)
        if form.is_valid():
            form.save()
            return redirect('bebidas')
    else:
        ingredientes_iniciales = bebida.ingredientes.values_list('id', flat=True)
        form = BebidaForm(instance=bebida, initial={'ingredientes': ingredientes_iniciales})
    
    return render(request, 'home/bebida_actualizar.html', {'form': form, 'bebida_id': bebida_id, 'categorias': categorias, 'ingredientes': ingredientes})


def bebida_eliminar(request, bebida_id):
    bebida = Bebida.objects.get(pk=bebida_id)
    bebida.delete()
    return redirect('bebidas')


def categoria_nueva(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = CategoriaForm()
    return render(request, 'home/Categoria_nueva.html', {'form': form})


def orden_nueva(request):
    ingredientes = Ingrediente.objects.all()
    tipos = Tipo.objects.all()
    categorias = Categoria.objects.all()
    bebidas = Bebida.objects.all()

    if request.method == 'POST':
        categoria_seleccionada = request.POST.get('categoria')
        if categoria_seleccionada:
            bebidas = Bebida.objects.filter(categoria__nombre=categoria_seleccionada)

    return render(request, 'home/Orden_nueva.html', {'categorias': categorias, 'bebidas': bebidas, 'ingredientes': ingredientes, 'tipos': tipos})


def obtener_ingredientes(request):
    ingredientes = Ingrediente.objects.all().values_list('nombre', flat=True)
    return JsonResponse({'ingredientes': list(ingredientes)})


def vista_principal(request):
    categorias = Categoria.objects.all()
    return render(request, 'prueba.html', {'categorias': categorias})

