from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .models import *
from .decorators import *
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from datetime import datetime


def landing(request):
    return render(request, "home/landing_page.html", {})


def ordenes(request):
    today = timezone.localdate()  # Obtener la fecha actual
    ventas_pendientes = Venta.objects.filter(estado='pendiente')
    ventas_completadas = Venta.objects.filter(estado='completada', fecha_venta__date=today)
    return render(request, 'home/Ordenes.html', {
        'ventas_pendientes': ventas_pendientes,
        'ventas_completadas': ventas_completadas
    })


def eliminar_orden(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.delete()
    return redirect('ordenes')


def menu(request):
    return render(request, "home/Menu.html", {})


def clientes(request):
    clientes_list = Cliente.objects.all()
    paginator = Paginator(clientes_list, 10)

    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

    return render(request, "home/Clientes.html", {'clientes': clientes})


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
    return render(request, 'home/Cliente_nuevo.html', {'form': form})


def clientes_actualizar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'home/Cliente_actualizar.html', {'form': form, 'cliente_id': cliente_id})


def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes')


def proveedores(request):
    proveedores_list = Proveedor.objects.all()
    paginator = Paginator(proveedores_list, 10)

    page_number = request.GET.get('page')
    proveedores = paginator.get_page(page_number)

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
    
    return render(request, 'home/Proveedores_actualizar.html', {'form': form, 'proveedor_id': proveedor_id})


def proveedores_eliminar(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.delete()
    return redirect('proveedores')


def inventario(request):
    ingredientes_list = Ingrediente.objects.all()  # Obtenemos todos los ingredientes
    paginator = Paginator(ingredientes_list, 5)  # Creamos un Paginator, 5 ingredientes por página

    page_number = request.GET.get('page')  # Obtenemos el número de página de los parámetros de la URL
    ingredientes = paginator.get_page(page_number)  # Obtenemos la página correspondiente

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
            messages.error(request, "Error al crear un ingrediente, inténtelo de nuevo")
    else:
        form = IngredienteForm()

    # Obtener el tipo seleccionado, si existe
    tipo_id = request.POST.get('tipo')
    ingredientes_tipo = []
    if tipo_id:
        # Filtrar ingredientes por tipo seleccionado
        ingredientes_tipo = Ingrediente.objects.filter(tipo_id=tipo_id)

    return render(request, 'home/Inventario_nuevo.html', {'form': form, 'tipos': tipos, 'proveedores': proveedores, 'ingredientes_tipo': ingredientes_tipo})


def obtener_ingredientes_por_tipo(request):
    if request.method == 'GET':
        tipo_id = request.GET.get('tipo_id')
        if tipo_id:
            ingredientes = Ingrediente.objects.filter(tipo_id=tipo_id)
            data = [{'id': ingrediente.id, 'nombre': ingrediente.nombre} for ingrediente in ingredientes]
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse([], safe=False)  # Devuelve una lista vacía si no se proporciona el tipo_id
    return JsonResponse({'error': 'Error en la solicitud'}, status=400)


def cargar_ingredientes_por_tipo(request):
    if request.method == 'GET':
        tipo_id = request.GET.get('tipo_id')
        if tipo_id:
            ingredientes = Ingrediente.objects.filter(tipo_id=tipo_id)
            data = [{'id': ingrediente.id, 'nombre': ingrediente.nombre} for ingrediente in ingredientes]
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse([], safe=False)  # Devuelve una lista vacía si no se proporciona el tipo_id
    return JsonResponse({'error': 'Error en la solicitud'}, status=400)


def seleccionar_ingredientes(request):
    tipos = Tipo.objects.all()
    return render(request, 'home/seleccionar_ingredientes.html', {'tipos': tipos})


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
    bebidas_list = Bebida.objects.all()
    paginator = Paginator(bebidas_list, 5)

    page_number = request.GET.get('page')
    bebidas = paginator.get_page(page_number)

    return render(request, "home/Bebidas.html", {'bebidas': bebidas})


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
    tamaños = TamañoBebida.objects.all()

    return render(request, 'home/Bebida_nueva.html', {
        'form': form, 
        'ingredientes': ingredientes, 
        'categorias': categorias,
        'tamaños': tamaños
    })


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
    
    return render(request, 'home/Bebida_actualizar.html', {'form': form, 'bebida_id': bebida_id, 'categorias': categorias, 'ingredientes': ingredientes})


def bebida_eliminar(request, bebida_id):
    bebida = Bebida.objects.get(pk=bebida_id)
    bebida.delete()
    return redirect('bebidas')


def categoria_nueva(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bebidas')
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
        else:
            bebida_id = request.POST.get('bebida_id')
            bebida = Bebida.objects.get(pk=bebida_id)
            cantidad = int(request.POST.get('cantidad'))
            precio_unitario = bebida.precio_base
            # Creamos un objeto DetalleVenta y lo guardamos
            detalle_venta = DetalleVenta.objects.create(bebida=bebida, cantidad=cantidad, precio_unitario=precio_unitario)
            # Añadimos el detalle de venta a la lista de detalles de la venta actual
            if 'venta_detalles' not in request.session:
                request.session['venta_detalles'] = []
            request.session['venta_detalles'].append(detalle_venta.id)

    return render(request, 'home/Orden_nueva.html', {'categorias': categorias, 'bebidas': bebidas, 'ingredientes': ingredientes, 'tipos': tipos})


def procesar_venta(request):
    if request.method == 'POST' and 'confirmar_venta' in request.POST:
        # Creamos un objeto Venta y lo guardamos
        venta = Venta.objects.create(total=0)
        # Recuperamos los detalles de venta de la sesión
        detalles_ids = request.session.get('venta_detalles', [])
        detalles_venta = DetalleVenta.objects.filter(id__in=detalles_ids)
        # Asignamos la venta a los detalles de venta y los guardamos
        for detalle_venta in detalles_venta:
            detalle_venta.venta = venta
            detalle_venta.save()
        # Actualizamos el total de la venta
        venta.total = venta.calcular_total()
        venta.save()
        # Limpiamos la sesión
        request.session['venta_detalles'] = []
        return JsonResponse({'success': True})  # Devuelve una respuesta JSON para indicar que la venta se procesó correctamente
    else:
        return JsonResponse({'success': False})  # Devuelve una respuesta JSON para indicar que hubo un error al procesar la venta


@csrf_exempt
def guardar_ingredientes(request):
    if request.method == 'POST':
        try:
            bebida_id = request.POST.get('bebidaId')
            ingredientes = json.loads(request.POST.get('ingredientes'))
            bebida = Bebida.objects.get(id=bebida_id)

            if 'venta_detalles' not in request.session:
                request.session['venta_detalles'] = []

            # Suponiendo que quieres agregar cada ingrediente con su cantidad a la venta
            for ing in ingredientes:
                ingrediente = Ingrediente.objects.get(id=ing['id'])
                cantidad = ing['cantidad']
                # Crear detalle de venta por cada tipo de ingrediente
                detalle_venta = DetalleVenta.objects.create(
                    bebida=bebida,
                    cantidad=cantidad,  # Usar la cantidad pasada del frontend
                    precio_unitario=bebida.precio_base  # Esto puede ajustarse si el precio depende de los ingredientes
                )
                request.session['venta_detalles'].append(detalle_venta.id)

            request.session.modified = True
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def obtener_ingredientes(request):
    ingredientes = Ingrediente.objects.all().values_list('nombre', flat=True)
    return JsonResponse({'ingredientes': list(ingredientes)})


def vista_principal(request):
    categorias = Categoria.objects.all()
    return render(request, 'prueba.html', {'categorias': categorias})


##### Prueba

def crear_venta(request):
    if request.method == 'POST':
        venta = Venta(
            fecha_venta=timezone.now(),
            total=0,
            estado='pendiente',
            detalles=''
        )
        venta.save()
        return JsonResponse({'success': True, 'venta_id': venta.id})
    else:
        venta_form = VentaForm()
    return render(request, 'home/crear_venta.html', {'venta_form': venta_form})


def agregar_detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        detalle_venta_form = DetalleVentaForm(request.POST)
        if detalle_venta_form.is_valid():
            detalle_venta = detalle_venta_form.save(commit=False)
            detalle_venta.venta = venta

            tamaño = detalle_venta_form.cleaned_data['tamaño']
            bebida = detalle_venta_form.cleaned_data['bebida']

            # Ajustar cantidad de leche según el tamaño de la bebida
            cantidad_a_restar = tamaño.cantidad_leche
            precio_extra = 0
            if tamaño.nombre.lower() == 'mediano':
                precio_extra = 10
            elif tamaño.nombre.lower() == 'grande':
                precio_extra = 20

            detalle_venta.precio_unitario += precio_extra
            detalle_venta.save()

            if venta.cliente:
                puntos_por_bebida = 100 * detalle_venta.cantidad
                venta.cliente.añadir_puntos(puntos_por_bebida)

            ingredientes_extra = request.POST.getlist('ingredientes_extra')
            if ingredientes_extra:
                puntos_por_ingredientes = 50 * len(ingredientes_extra)
                venta.cliente.añadir_puntos(puntos_por_ingredientes)

            # Buscar el ingrediente de leche correspondiente
            ingrediente_leche = Ingrediente.objects.filter(tipo__nombre='Leche').first()
            if ingrediente_leche:
                # Conversión de unidades (ejemplo: de onzas a litros)
                if ingrediente_leche.unidad == 'onzas' and ingrediente_leche.unidad_original == 'litros':
                    cantidad_convertida = Decimal(cantidad_a_restar) / Decimal(33.814)  # 1 litro = 33.814 onzas
                elif ingrediente_leche.unidad == 'gramos' and ingrediente_leche.unidad_original == 'kilogramos':
                    cantidad_convertida = Decimal(cantidad_a_restar) / Decimal(1000)  # 1 kilogramo = 1000 gramos
                else:
                    cantidad_convertida = Decimal(cantidad_a_restar)

                # Restar la cantidad convertida del inventario disponible
                ingrediente_leche.cantidad_disponible -= cantidad_convertida
                ingrediente_leche.save()

                DetalleVentaIngrediente.objects.create(detalle_venta=detalle_venta, ingrediente=ingrediente_leche, cantidad=cantidad_a_restar)

            venta.save()  # Actualiza el total de la venta
            return redirect('agregar_detalle_venta', venta_id=venta.id)
    else:
        detalle_venta_form = DetalleVentaForm()

    bebidas = Bebida.objects.all()
    ingredientes = Ingrediente.objects.all()
    return render(request, 'home/agregar_detalle_venta.html', {
        'venta': venta,
        'detalle_venta_form': detalle_venta_form,
        'bebidas': bebidas,
        'ingredientes': ingredientes
    })


def actualizar_venta_info(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        telefono = data.get('telefono')
        detalles = data.get('detalles')

        if telefono:
            cliente = Cliente.objects.filter(telefono=telefono).first()
            if cliente:
                venta.cliente = cliente
            else:
                return JsonResponse({'success': False, 'error': 'Cliente no encontrado'})

        if detalles:
            venta.detalles = detalles

        venta.save()
        return JsonResponse({'success': True, 'total': str(venta.total)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def agregar_ingredientes(request, detalle_venta_id):
    detalle_venta = get_object_or_404(DetalleVenta, id=detalle_venta_id)
    
    if request.method == 'POST':
        ingrediente_id = request.POST.get('ingrediente_id')
        cantidad = request.POST.get('cantidad')
        action = request.POST.get('action')

        if action == 'add':
            ingrediente_form = DetalleVentaIngredienteForm(request.POST)
            if ingrediente_form.is_valid():
                detalle_ingrediente = ingrediente_form.save(commit=False)
                detalle_ingrediente.detalle_venta = detalle_venta
                detalle_ingrediente.save()
                return redirect('agregar_ingredientes', detalle_venta_id=detalle_venta.id)
        elif action == 'update' and ingrediente_id and cantidad:
            detalle_ingrediente = get_object_or_404(DetalleVentaIngrediente, id=ingrediente_id)
            detalle_ingrediente.cantidad = cantidad
            detalle_ingrediente.save()
            return redirect('agregar_ingredientes', detalle_venta_id=detalle_venta.id)
        elif action == 'delete' and ingrediente_id:
            detalle_ingrediente = get_object_or_404(DetalleVentaIngrediente, id=ingrediente_id)
            detalle_ingrediente.delete()
            return redirect('agregar_ingredientes', detalle_venta_id=detalle_venta.id)
    else:
        ingrediente_form = DetalleVentaIngredienteForm()

    return render(request, 'home/agregar_ingredientes.html', {
        'detalle_venta': detalle_venta,
        'ingrediente_form': ingrediente_form
    })


def ver_orden(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return render(request, 'home/ver_orden.html', {'venta': venta})


def finalizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.estado = 'completada'
    venta.save()
    return redirect('ordenes')


def poner_venta_pendiente(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    venta.estado = 'pendiente'
    venta.save()
    return redirect('ordenes')


def cancelar_venta(request, venta_id):
    try:
        venta = Venta.objects.get(id=venta_id)
        # Si decides eliminar la venta descomenta la siguiente línea
        venta.delete()
        return redirect('ordenes')  # Cambia 'ruta_a_redirigir' por la ruta donde quieres que el usuario sea redirigido
    except Venta.DoesNotExist:
        return redirect('ordenes')  # Manejo en caso de que la venta ya no exista


def ventas(request):
    ventas = Venta.objects.filter(estado='pendiente')
    venta_form = VentaForm()
    detalle_venta_form = DetalleVentaForm()
    ingrediente_form = DetalleVentaIngredienteForm()
    return render(request, 'home/venta_integrada.html', {
        'ventas': ventas,
        'venta_form': venta_form,
        'detalle_venta_form': detalle_venta_form,
        'ingrediente_form': ingrediente_form
    })


def buscar_clientes(request):
    telefono = request.GET.get('telefono', '')
    clientes = Cliente.objects.filter(telefono__icontains=telefono)[:5]  # Limita a los primeros 5 resultados
    data = [{'nombre': cliente.nombre, 'telefono': cliente.telefono} for cliente in clientes]
    return JsonResponse({'clientes': data})


def obtener_precio_bebida(request):
    bebida_id = request.GET.get('bebida')
    tamaño_id = request.GET.get('tamaño')
    
    bebida = get_object_or_404(Bebida, id=bebida_id)
    tamaño = get_object_or_404(TamañoBebida, id=tamaño_id)
    
    precio_base = bebida.precio_base
    precio_extra = 0
    
    if tamaño.nombre.lower() == 'mediano':
        precio_extra = 10
    elif tamaño.nombre.lower() == 'grande':
        precio_extra = 20
    
    precio_total = precio_base + precio_extra
    
    return JsonResponse({'success': True, 'precio_base': str(precio_base), 'precio_total': str(precio_total)})


def reporte_ventas(request):
    hoy = timezone.now().date()
    fecha_inicio = hoy
    fecha_fin = hoy

    if request.method == 'POST':
        form = ReporteVentaForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
    else:
        form = ReporteVentaForm(initial={'fecha_inicio': hoy, 'fecha_fin': hoy})

    ventas = Venta.objects.filter(fecha_venta__date__range=[fecha_inicio, fecha_fin])
    total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0
    total_bebidas_vendidas = DetalleVenta.objects.filter(venta__in=ventas).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    detalles_ventas = DetalleVenta.objects.filter(venta__in=ventas)

    # Calcular el inventario usado y los ingresos de ingredientes extras
    total_ingresos_extras = 0
    total_ingredientes_usados = {}
    for detalle in detalles_ventas:
        for ingrediente in detalle.ingredientes_extra.all():
            cantidad_usada = detalle.detalleventaingrediente_set.get(ingrediente=ingrediente).cantidad
            total_ingresos_extras += cantidad_usada * ingrediente.precio_extra
            if ingrediente.nombre in total_ingredientes_usados:
                total_ingredientes_usados[ingrediente.nombre] += cantidad_usada
            else:
                total_ingredientes_usados[ingrediente.nombre] = cantidad_usada

    return render(request, 'home/reporte_ventas.html', {
        'form': form,
        'ventas': ventas,
        'total_ventas': total_ventas,
        'total_bebidas_vendidas': total_bebidas_vendidas,
        'detalles_ventas': detalles_ventas,
        'total_ingresos_extras': total_ingresos_extras,
        'total_ingredientes_usados': total_ingredientes_usados,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


def generar_reporte_pdf(request, fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    ventas = Venta.objects.filter(fecha_venta__date__range=[fecha_inicio, fecha_fin])
    total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0
    total_bebidas_vendidas = DetalleVenta.objects.filter(venta__in=ventas).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    detalles_ventas = DetalleVenta.objects.filter(venta__in=ventas)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, height - 50, "Reporte de Ventas: Detalle Completo")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, height - 80, f"Fecha de Inicio: {fecha_inicio.strftime('%d/%m/%Y')}")
    pdf.drawString(30, height - 100, f"Fecha de Fin: {fecha_fin.strftime('%d/%m/%Y')}")
    pdf.drawString(30, height - 120, f"Total de Ventas: ${total_ventas:.2f}")
    pdf.drawString(30, height - 140, f"Total de Bebidas Vendidas: {total_bebidas_vendidas}")

    # Detalles de Ventas
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(30, height - 180, "Detalles de Ventas:")
    y = height - 200
    pdf.setFont("Helvetica", 10)
    for venta in ventas:
        pdf.drawString(30, y, f"ID Venta: {venta.id} - Fecha: {venta.fecha_venta.strftime('%d/%m/%Y %H:%M')} - Cliente: {venta.cliente} - Total: ${venta.total:.2f}")
        y -= 20
        for detalle in venta.detalleventa_set.all():
            pdf.drawString(50, y, f"Bebida: {detalle.bebida.nombre}, Cantidad: {detalle.cantidad}, Precio Unitario: ${detalle.precio_unitario:.2f}")
            y -= 20
        y -= 10

    # Información sobre Ingredientes Extras
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(30, y, "Ingredientes Extras Usados:")
    y -= 20
    pdf.setFont("Helvetica", 10)
    for detalle in detalles_ventas:
        for ingrediente in detalle.ingredientes_extra.all():
            detalle_ingrediente = detalle.detalleventaingrediente_set.get(ingrediente=ingrediente)
            pdf.drawString(50, y, f"Ingrediente: {ingrediente.nombre}, Cantidad: {detalle_ingrediente.cantidad}, Costo Extra: ${ingrediente.precio_extra * detalle_ingrediente.cantidad:.2f}")
            y -= 20
        y -= 10

    pdf.showPage()
    pdf.save()
    return response

