import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CreateTicketForm
from .models import Ticket

User = get_user_model()

#Create Tickets View
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.customer = request.user
            while not new_ticket.ticket_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    new_ticket.ticket_id = id
                    new_ticket.save()
                    messages.success(request, 'Your ticket has been submitted. A Support Engineer would reach out soon.')
                    return redirect('customer-active-tickets') # This will redirect to customers ongoing tickets
                    # break
                except IntegrityError: # handle errors gracefully - to catch the IntegrityError that might arise when trying to save the ticket with a duplicate ticket ID.
                    continue
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request, 'tickets/create_ticket.html', context)

def customer_active_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('created_on')
    active_tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).count
    context = {'tickets':tickets, 'active_tickets':active_tickets}
    return render(request, 'tickets/customer_active_tickets.html', context)