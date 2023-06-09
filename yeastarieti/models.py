from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    receiver = models.CharField(max_length=9)
    send_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Message ID: {self.message_id}, Sender: {self.sender.username}, Receiver: {self.receiver}'




    