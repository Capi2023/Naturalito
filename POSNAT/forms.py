from django import forms
from .models import *

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'compañia', 'direccion', 'correo', 'numero']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'correo', 'puntos']  # Removido 'venta'

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
        # Verificar si ya existe un ingrediente con el mismo nombre
        if Ingrediente.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe un ingrediente con este nombre.")
        return nombre.upper()

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        proveedor = cleaned_data.get('proveedor')
        # Realizar verificaciones adicionales si es necesario
        return cleaned_data


class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['nombre', 'detalles']


class BebidaForm(forms.ModelForm):
    class Meta:
        model = Bebida
        fields = ['nombre', 'categoria', 'imagen', 'ingredientes', 'precio_base', 'detalles']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'detalles']


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['bebida', 'cantidad', 'precio_unitario']


class BebidaIngredientesForm(forms.ModelForm):
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingrediente.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Bebida
        fields = ['nombre', 'categoria', 'imagen', 'precio_base', 'detalles', 'ingredientes']

