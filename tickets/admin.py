
from django.contrib import admin
from .models import Ticket
from django_summernote.admin import SummernoteModelAdmin


class TicketAdmin(SummernoteModelAdmin):
    list_display = ('ticket_id', 'ticket_title', 'customer', 'created_on', 'status')  # What fields to display in the list view
    search_fields = ['ticket_id', 'ticket_title', 'customer__email']  # Make some fields searchable
    list_filter = ['status', 'customer']  # Add filters for easier admin filtering

admin.site.register(Ticket, TicketAdmin)
