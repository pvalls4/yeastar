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
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'm-3 p-0.5 text-blue-800 rounded-md'}))
    password = forms.CharField(label='Contraseña', widget=forms.TextInput(attrs={'type': 'password', 'class': 'p-0.5 text-blue-800 rounded-md'}))
# myfield = forms.CharField(widget=forms.TextInput(attrs={'class': 'myfieldclass'}))

class MessageForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'm-3 p-0.5 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'Escribe tu SMS aquí...'}))
    receiver = forms.CharField(widget=forms.TextInput(attrs={'type': 'number', 'max_length':'9','class': 'p-0.5 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'Escribe el número destino.'}))
    
    def clean_my_field(self):
        data = self.cleaned_data['receiver']
        if len(data) != 9:
            raise forms.ValidationError("El campo debe tener una longitud de 9 carácteres.")
        return data
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


