from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Añade los campos adicionales que deseas
    max_sms = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=9, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    receiver = models.CharField(max_length=9)
    send_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Message ID: {self.message_id}, Sender: {self.sender.username}, Receiver: {self.receiver}'



    