from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import Widget
from django.core.validators import MinLengthValidator, MaxLengthValidator
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
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'm-3 p-0.5 px-1 text-blue-800 rounded-md'}))
    password = forms.CharField(label='Contraseña', widget=forms.TextInput(attrs={'type': 'password', 'class': 'p-0.5 px-1 text-blue-800 rounded-md'}))
# myfield = forms.CharField(widget=forms.TextInput(attrs={'class': 'myfieldclass'}))

class MessageForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'p-0.5 px-1 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'Escribe tu SMS aquí...'}))
    receiver = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'number','class': 'p-0.5 px-1 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'Escribe el número destino.'}))
    contact = forms.ModelChoiceField(label="Contacto", queryset=None, widget=forms.HiddenInput())
#validators=[MinLengthValidator(9), MaxLengthValidator(9)]
    class Meta:
        model = Message
        fields = ['text', 'receiver', 'contact']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact'].queryset = Contact.objects.filter(user=user)

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label="E-Mail", max_length=254, widget=forms.EmailInput(attrs={'class': 'm-2 p-0.5 px-1.5 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'Correo electrónico', 'title': 'Ingrese una dirección de correo válida.'}))
    phone = forms.IntegerField(label="Teléfono",validators=[MinLengthValidator(9), MaxLengthValidator(9)],  widget=forms.TextInput(attrs={'class': 'm-2 p-0.5 px-1.5 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'Teléfono', 'title': 'Ingrese su número de teléfono.'}))
    department = forms.CharField(label="Departamento", max_length=100,  widget=forms.TextInput(attrs={'class': 'm-2 p-0.5 px-1.5 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'Departamento', 'title': 'Ingrese el departamento al que pertenece.'}))
    max_sms = forms.IntegerField(label="Número máximo de SMS/día",  widget=forms.TextInput(attrs={'class': 'm-2 p-0.5 px-1.5 text-blue-800 rounded-md placeholder:font-italic', 'placeholder':'SMS máximos', 'title': 'Ingrese el número máximo de mensajes que puede enviar al día.'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['username'].widget.attrs['class'] = 'm-2 p-0.5 px-1.5 text-blue-800 rounded-md placeholder:font-italic'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['username'].widget.attrs['title'] = 'Ingrese su nombre de usuario.'
        self.fields['username'].help_text = ''

        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].widget.attrs['class'] = 'm-2 p-0.5 px-1.5 text-blue-800 rounded-md placeholder:font-italic'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].widget.attrs['title'] = 'Ingrese su contraseña.'
        self.fields['password1'].help_text = ''

        self.fields['password2'].label = 'Repita su contraseña'
        self.fields['password2'].widget.attrs['class'] = 'm-2 p-0.5 px-1.5 text-blue-800 rounded-md placeholder:font-italic'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repita la contraseña'
        self.fields['password2'].widget.attrs['title'] = 'Ingrese de nuevo su contraseña.'
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'department', 'max_sms')


