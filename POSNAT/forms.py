from django import forms
from .models import *

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'compañia', 'direccion', 'correo', 'numero']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'correo', 'puntos', 'venta']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if Cliente.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError('Este número de teléfono ya está registrado.')
        return telefono

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = '__all__'
        """
        fields = ['nombre', 'tipo', 'imagen', 'precio_extra', 'cantidad_extra', 'cantidad_disponible', 'cantidad_minima', 'proveedor', 'detalles']
        """
        

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

