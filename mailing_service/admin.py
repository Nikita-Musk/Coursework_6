from django.contrib import admin

from mailing_service.models import Mailing, Message, Client


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'period', 'status', 'message',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','subject', 'body',)
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment',)
