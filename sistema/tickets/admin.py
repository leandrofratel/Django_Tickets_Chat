from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['codigo_incidente', 'status', 'criado_em']
    list_filter = ['status']
    serch_fields = ['codigo_incidente']