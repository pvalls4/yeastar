import os
import requests
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import *
from .models import *
from .serializers import * 

from urllib.parse import quote

from django.contrib.auth import authenticate

from django.utils.crypto import get_random_string

api_account = os.environ.get('API_ACCOUNT')
api_password = os.environ.get('API_PASSWORD')
yestar_ip = os.environ.get('YEASTAR_IP')
        
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
                    return redirect('/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('/')
    

# Create your views here.        
def logout_view(request):
	logout(request)
	return redirect("/login")

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
    user = request.user
    contacts = Contact.objects.filter(user=user)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid() and (user.current_sms < user.max_sms):
            try: 
                # Obtener los datos del formulario
                receiver = form.cleaned_data['receiver']
                text = form.cleaned_data['text']

                # Codificar el texto en URL Encode
                encoded_text = quote(text)

                # Construir la URL de la API de Yeastar con los datos del formulario
                api_url = f"http://{yeastar_ip}/cgi/WebCGI?1500101=account={api_account}&password={api_password}&port=1&destination=34{receiver}&content={encoded_text}"
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
                    remain_sms = user.max_sms - user.current_sms
                    exists = contacts.filter(num_contact=receiver).exists()
                    contact_saved = None
                    if exists:
                        contact_saved = contacts.get(num_contact=receiver).contact
                    #Redirecciona a la página de éxito después de enviar el formulario
                    content2 = {
                        'user': user,
                        'message': message,
                        'contact_saved': contact_saved,
                        'remain_sms': remain_sms
                    }
                    return render(request, 'message_success.html', content2)
                else:
                    raise Http404
            except requests.exceptions.RequestException as e:
                #error_message = f"Error de conexión: {str(e)}"
                return render(request, 'message_failure.html')
    else: 
        form = MessageForm()
        remain_sms = user.max_sms - user.current_sms
        content = {
            'user': user,
            'remain_sms' : remain_sms,
            'contacts': contacts,
            'form' : form
        }
    return render(request, 'dashboard.html', content)

def api_sendsms(request):
    username = request.GET.get('username')
    api_token = request.GET.get('api_token')
    text = request.GET.get('text')
    # Codificar el texto en URL Encode
    encoded_text = quote(text)
    receiver = request.GET.get('receiver')
    user = User.objects.get(username=username)
    if api_token == user.api_token:
        # Verificar si user.current_sms es menor que user.max_sms
        if user.current_sms >= user.max_sms:
            return HttpResponse('Límite de SMS alcanzado', status=403)

        #Guardamos el registro en la tabla Message
        message = Message(sender=user, text=text, receiver=receiver)
        message.save()

        # Actualizar el contador de mensajes enviados por el usuario
        user.current_sms += 1
        user.save()
        api_url = f"http://{yeastar_ip}/cgi/WebCGI?1500101=account={api_account}&password={api_password}&port=1&destination=34{receiver}&content={encoded_text}"

        # Realizar la solicitud a la API de Yeastar
        response = requests.get(api_url)
        remain_sms = user.max_sms - user.current_sms
        return HttpResponse(f'Mensaje enviado a la API de Yeastar. Te quedan {remain_sms} mensajes por mandar hoy.')
    else:
        return HttpResponse('Credenciales inválidas', status=401)

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

@login_required   
def add_contact(request):
    if request.method == 'POST':
        form = AddContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('/')  # Redirige a la página principal
    else:
        form = AddContactForm()
    
    return render(request, 'add_contact.html', {'form': form})

@login_required   
def contacts(request):
    contacts=Contact.objects.filter(user=request.user).order_by('contact')
    print(contacts)
    content = {
        'contacts': contacts
    }
    return render(request, 'contacts.html', content)

def delete_contact(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact.delete()
    return redirect('contacts')
