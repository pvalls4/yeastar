from django.shortcuts import render, redirect
import requests
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views

from .models import *
from .serializers import * 
from rest_framework import viewsets
from django.contrib.auth.models import Permission
from rest_framework import permissions
import os, mimetypes

from urllib.parse import quote


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.utils.crypto import get_random_string

#class MyAuthForm(AuthenticationForm):
#	error_messages = {
#		'invalid_login': (
#			"Asegurate de introducir el correo y la contraseña correctamente."
#			" Ten en cuenta las máyusculas."
#		),
#		'inactive': ("El ususario no esta activo"),
#	}

#class LoginView(auth_views.LoginView):
#	form_class = LoginForm
#	authentication_form = MyAuthForm
#	template_name = 'login.html'
        
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')  # Cambia 'home' por la ruta a tu página principal
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('/')
    

        
def logout_view(request):
	logout(request)
	return render(request, "logout.html")
# Create your views here.

@login_required
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirecciona al inicio de sesión después de crear el usuario
    else:
        form = CreateUserForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
def dashboard(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid() and user.current_sms<user.max_sms:
            try: 
                # Obtener los datos del formulario
                receiver = form.cleaned_data['receiver']
                text = form.cleaned_data['text']

                # Codificar el texto en URL Encode
                encoded_text = quote(text)

                # Construir la URL de la API de Yeastar con los datos del formulario
                api_url = f"http://192.168.5.150/cgi/WebCGI?1500101=account=ietiyeastar&password=Projectieti23&port=1&destination=34{receiver}&content={encoded_text}"

                # Enviar la solicitud a la API de Yeastar
                response = requests.get(api_url)
                if response.status_code == 200:
                    #Guardamos el mensaje en la base de datos
                    message = form.save(commit=False)
                    message.sender = request.user
                    message.save()

                    #Sumamos uno al contador de mensajes del usuario
                    user = request.user
                    user.current_sms += 1
                    user.save()
                    print("Testing")
                    print(response)

                    #Redirecciona a la página de éxito después de enviar el formulario
                    return redirect('message_success')
                else:
                    raise Http404
            except requests.exceptions.RequestException as e:
                error_message = f"Error de conexión: {str(e)}"
                return redirect('message_failure.html')
    else:
        form = MessageForm()
        remain_sms = user.max_sms - user.current_sms
        content = {
            'user': user,
            'remain_sms' : remain_sms,
            'form' : form
        }
    return render(request, 'dashboard.html', content)

def api_sendsms(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    text = request.GET.get('text')
    receiver = request.GET.get('receiver')

    # Codificar el texto en URL Encode
    encoded_text = quote(text)

    # Verificar si el usuario y la contraseña son válidos
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse('Credenciales inválidas', status=401)

    # Verificar si user.current_sms es menor que user.max_sms
    if user.current_sms >= user.max_sms:
        return HttpResponse('Límite de SMS alcanzado', status=403)

    #Guardamos el registro en la tabla Message
    message = Message(sender=user, text=text, receiver=receiver)
    message.save()

    # Actualizar el contador de mensajes enviados por el usuario
    user.current_sms += 1
    user.save()
    api_url = f"http://192.168.5.150/cgi/WebCGI?1500101=account=ietiyeastar&password=Projectieti23&port=1&destination=34{receiver}&content={encoded_text}"

    # Realizar la solicitud a la API de Yeastar
    response = requests.get(api_url)
    remain_sms = user.max_sms - user.current_sms
    return HttpResponse(f'Mensaje enviado a la API de Yeastar. Te quedan {remain_sms} mensajes por mandar hoy.')

@login_required
def message_success(request):
    user = User.objects.get(pk=request.user.pk)
    remain_sms = user.max_sms - user.current_sms
    content = {
        'user': user,
        'remain_sms' : remain_sms,
    }
    return render(request, 'message_success.html', content)

@login_required
def token(request):
    user = request.user
    content = {
        'user': user
    }
    if request.method == 'POST':
        # Generar un nuevo token
        new_token = get_random_string(length=64)
        user.api_token = new_token
        user.save()
        messages.success(request, 'El token API se ha cambiado exitosamente.')
        return redirect('/token')  # Redirecciona a la página de opciones de token
    else:
        return render(request, 'token.html', content)