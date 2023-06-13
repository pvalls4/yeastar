from django.contrib import admin
from .models import User, Message, Contact

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'text', 'receiver', 'send_date')
admin.site.register(Message, MessageAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'department', 'max_sms', 'current_sms')
admin.site.register(User, UserAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'user', 'contact', 'num_contact')
admin.site.register(Contact, ContactAdmin)

