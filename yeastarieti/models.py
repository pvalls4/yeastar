import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator, MaxLengthValidator

class User(AbstractUser):
    # Añade los campos adicionales que deseas
    max_sms = models.PositiveIntegerField(default=0)
    current_sms = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=9, validators=[
            MinLengthValidator(9, message='El número de teléfono debe tener 9 dígitos.'),
            MaxLengthValidator(9, message='El número de teléfono debe tener 9 dígitos.')
        ])
    department = models.CharField(max_length=100, blank=True)
    api_token = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.username

@receiver(pre_save, sender=User)
def generate_api_token(sender, instance, **kwargs):
    if not instance.api_token:
        # Generar un token aleatorio
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        instance.api_token = token

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    receiver = models.CharField(max_length=9, validators=[
            MinLengthValidator(9, message='El número de teléfono debe tener 9 dígitos.'),
            MaxLengthValidator(9, message='El número de teléfono debe tener 9 dígitos.')
        ])
    send_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Message ID: {self.message_id}, Sender: {self.sender.username}, Receiver: {self.receiver}'

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20)
    num_contact = models.CharField(max_length=9, validators=[
            MinLengthValidator(9, message='El número de teléfono debe tener 9 dígitos.'),
            MaxLengthValidator(9, message='El número de teléfono debe tener 9 dígitos.')
        ])


    