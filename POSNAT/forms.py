from django import forms
from .models import *

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'compañía', 'direccion', 'correo', 'numero']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'correo', 'puntos']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if Cliente.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError('Este número de teléfono ya está registrado.')
        return telefono


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Ingrediente.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un ingrediente con este nombre.")
        return nombre.upper()


class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['nombre', 'detalles']


class BebidaForm(forms.ModelForm):
    class Meta:
        model = Bebida
        fields = ['nombre', 'categoria', 'imagen', 'ingredientes', 'precio_base', 'detalles', 'disponible', 'tamaños']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'detalles']


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'


class DetalleVentaForm(forms.ModelForm):
    tamaño = forms.ModelChoiceField(queryset=TamañoBebida.objects.all(), required=True, label='Tamaño')

    class Meta:
        model = DetalleVenta
        fields = ['bebida', 'cantidad', 'precio_unitario', 'comentarios', 'tamaño']



class DetalleVentaIngredienteForm(forms.ModelForm):
    class Meta:
        model = DetalleVentaIngrediente
        fields = ['detalle_venta', 'ingrediente', 'cantidad']


class ReporteVentaForm(forms.ModelForm):
    class Meta:
        model = ReporteVenta
        fields = ['fecha_inicio', 'fecha_fin', 'tipo_periodo', 'total_ventas', 'total_bebidas_vendidas', 'cantidad_de_clientes']

