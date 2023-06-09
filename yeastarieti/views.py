from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views

from .models import *
from .serializers import * 
from rest_framework import viewsets
from django.contrib.auth.models import Permission
from rest_framework import permissions
import os, mimetypes



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

#class LoginView(APIView):
#    def post(self, request):
#        username = request.data.get('username')
#        password = request.data.get('password')

#        user = authenticate(username=username, password=password)

#        if user is not None:
#            token, _ = Token.objects.get_or_create(user=user)
#            return Response({'token': token.key})
#        else:
#            return Response({'error': 'Credenciales inválidas'}, status=401)


class MyAuthForm(AuthenticationForm):
	error_messages = {
		'invalid_login': (
			"Asegurate de introducir el correo y la contraseña correctamente."
			" Ten en cuenta las máyusculas."
		),
		'inactive': ("El ususario no esta activo"),
	}

class LoginView(auth_views.LoginView):
	form_class = LoginForm
	authentication_form = MyAuthForm
	template_name = 'login.html'
# Create your views here.

def home(request):
    content = {
        'nombre': 'John',
        'edad': 30,
    }
    return render(request, 'home.html', content)

@login_required
def dashboard(request):
    user = request.user.username
    content = {
        'nombre': user,
        'edad': 30,
    }
    return render(request, 'dashboard.html', content)