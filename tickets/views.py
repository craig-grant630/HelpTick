import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CreateTicketForm, AssignTicketForm
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
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on') #sort via create on date in reverse andticket has not been resolved
    active_tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).count
    context = {'tickets':tickets, 'active_tickets':active_tickets}
    return render(request, 'tickets/customer_active_tickets.html', context)

# To view tickets in more details
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id) # ticket with a certain ID
    context = {'ticket':ticket}
    return render(request, 'tickets/ticket_details.html', context)

# View tickets that have not been assigned engineers
def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_engineer=False) # ticket model filtered by not assigned to engineer
    context = {'tickets':tickets}
    return render(request, 'tickets/ticket_queue.html', context)

def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket) # pre-fill the form with the current values of ticket
        if form.is_valid():
            assigning = form.save(commit=False) #If form has correct details then save but do not commit
            assigning.is_assigned_to_engineer = True
            assigning.status = 'Active' # when assigned to engineer the status changes to Active
            assigning.save() #fully commit the save
            messages.success(request, f'Ticket has been assigned to {assigning.engineer}')
            return redirect('ticket-queue')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-ticket')
    else: # GET 
        form = AssignTicketForm(instance=ticket)
        form.fields['engineer'].queryset = User.objects.filter(is_engineer=True)
        context = {'form':form, 'ticket':ticket}
        return render(request, 'tickets/assign_ticket.html', context)