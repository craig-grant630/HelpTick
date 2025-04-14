import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CreateTicketForm, AssignTicketForm
from .models import Ticket
from django.core.paginator import Paginator

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
    ticket_list = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')
    paginator = Paginator(ticket_list, 8)  # Show 8 tickets per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    active_tickets = ticket_list.count()
    context = {
        'tickets': page_obj.object_list, 
        'active_tickets': active_tickets,
        'page_obj': page_obj,             # for pagination controls
    }
    return render(request, 'tickets/customer_active_tickets.html', context)

# To view tickets in more details
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id) # ticket with a certain ID
    context = {'ticket':ticket}
    return render(request, 'tickets/ticket_details.html', context)

def ticket_queue(request):
    # Get the search query from the GET parameters
    search_query = request.GET.get('search', '')
    
    if search_query:
        tickets = Ticket.objects.filter(
            is_assigned_to_engineer=False,
            ticket_id__icontains=search_query  # Filters based on ticket id
        )
    else:
        tickets = Ticket.objects.filter(is_assigned_to_engineer=False)
    
    context = {'tickets': tickets, 'search_query': search_query}
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

def engineer_active_tickets(request):
    ticket_list = Ticket.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_on')
    paginator = Paginator(ticket_list, 8)  # Show 8 tickets per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    active_tickets = ticket_list.count()
    context = {
        'tickets': page_obj.object_list, 
        'active_tickets': active_tickets,
        'page_obj': page_obj,             # for pagination controls
    }
    return render(request, 'tickets/engineer_active_tickets.html', context)

def resolve_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs  
        ticket.is_resolved = True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request, 'Ticket is now resolved and closed')
        return redirect('dashboard')

def customer_resolved_tickets(request):
    ticket_list = Ticket.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')
    paginator = Paginator(ticket_list, 8)  # Show 8 tickets per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    resolved_tickets = ticket_list.count()
    context = {
        'tickets': page_obj.object_list, 
        'resolved_tickets': resolved_tickets,
        'page_obj': page_obj,             # for pagination controls
    }
    return render(request, 'tickets/customer_resolved_tickets.html', context)

def engineer_resolved_tickets(request):
    ticket_list = Ticket.objects.filter(engineer=request.user, is_resolved=True).order_by('-created_on')
    paginator = Paginator(ticket_list, 8)  # Show 4 tickets per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    resolved_tickets = ticket_list.count()
    context = {
        'tickets': page_obj.object_list, 
        'resolved_tickets': resolved_tickets,
        'page_obj': page_obj,             # for pagination controls
    }
    return render(request, 'tickets/engineer_resolved_tickets.html', context)