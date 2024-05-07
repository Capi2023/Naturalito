from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import *

def login_user(request):
    if request.method == "POST":
        username = request.POST['usuario']  # Aquí corregí el nombre del campo de usuario
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, "El usuario no existe. Por favor, inténtalo de nuevo.")
            return render(request, 'authenticate/login.html', {})
    else:
        return render(request, 'authenticate/login.html', {})
