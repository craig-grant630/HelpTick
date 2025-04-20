
from django.contrib import admin
from .models import Ticket
from django_summernote.admin import SummernoteModelAdmin


class TicketAdmin(SummernoteModelAdmin):
    # What fields to display in the list view
    list_display = ('ticket_id', 'ticket_title', 'customer', 'created_on',
                    'status')
    # Make some fields searchable
    search_fields = ['ticket_id', 'ticket_title', 'customer__email']
    # Add filters for easier admin filtering
    list_filter = ['status', 'customer']


admin.site.register(Ticket, TicketAdmin)
