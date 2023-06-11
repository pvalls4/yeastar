from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import *
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')

# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'mb-4 mt-4 ml-[1.4%]'}))
    password = forms.CharField(label='Contraseña', widget=forms.TextInput(attrs={'type': 'password'}))
# myfield = forms.CharField(widget=forms.TextInput(attrs={'class': 'myfieldclass'}))

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'receiver']

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingrese una dirección de correo válida.')
    phone = forms.CharField(max_length=9, help_text='Requerido. Ingrese su número de teléfono.')
    department = forms.CharField(max_length=100, help_text='Requerido. Ingrese su departamento.')
    max_sms = forms.IntegerField(help_text='Requerido. Ingrese el número máximo de mensajes que puede enviar al día.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'department', 'max_sms')


