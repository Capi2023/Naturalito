from functools import wraps
from django.http import JsonResponse
from .models import *

def agregar_ingrediente(func):
    @wraps(func)
    def wrapper(request, bebida_id, ingrediente_id, cantidad):
        # Aquí puedes agregar la lógica para agregar el ingrediente a la bebida
        return func(request, bebida_id, ingrediente_id, cantidad)
    return wrapper