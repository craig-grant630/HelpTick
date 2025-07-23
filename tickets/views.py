import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import CreateTicketForm, AssignTicketForm, EditTicketForm
from .models import Ticket

User = get_user_model()


# Create Tickets View
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.customer = request.user
            while not new_ticket.ticket_id:
                ticket_id = ''.join(random.choices(string.digits, k=6))
                try:
                    new_ticket.ticket_id = ticket_id
                    new_ticket.save()
                    messages.success(
                        request,
                        'Your ticket has been submitted. A Support Engineer '
                        'would reach out soon.'
                    )
                    return redirect('customer-active-tickets')
                except IntegrityError:
                    continue
        else:
            messages.warning(
                request,
                'Something went wrong. Please check form errors'
            )
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'tickets/create_ticket.html', context)

@login_required
def customer_active_tickets(request):
    ticket_list = Ticket.objects.filter(
        customer=request.user,
        is_resolved=False
    ).order_by('-created_on')

    paginator = Paginator(ticket_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tickets': page_obj.object_list,
        'active_tickets': ticket_list.count(),
        'page_obj': page_obj,
    }
    return render(request, 'tickets/customer_active_tickets.html', context)

@login_required
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if (
        request.user != ticket.customer and
        request.user != ticket.engineer and
        not request.user.is_superuser
    ):
        messages.error(request, "You are not allowed to edit this ticket.")
        return redirect('dashboard')
    return render(request, 'tickets/ticket_details.html', {'ticket': ticket})

@login_required
def ticket_queue(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not allowed to view this page")
        return redirect('dashboard')
    search_query = request.GET.get('search', '')
    tickets = Ticket.objects.filter(
        is_assigned_to_engineer=False,
        ticket_id__icontains=search_query
    ) if search_query else Ticket.objects.filter(
        is_assigned_to_engineer=False
    )

    return render(
        request,
        'tickets/ticket_queue.html',
        {'tickets': tickets, 'search_query': search_query}
    )

@login_required
def assign_ticket(request, ticket_id):
    if not request.user.is_superuser:
        messages.error(request, "You are not allowed to view this page")
        return redirect('dashboard')
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            assigning = form.save(commit=False)
            assigning.is_assigned_to_engineer = True
            assigning.status = 'Active'
            assigning.save()
            messages.success(
                request,
                f'Ticket has been assigned to {assigning.engineer}'
            )
            return redirect('ticket-queue')
        else:
            messages.warning(
                request,
                'Something went wrong. Please check form input'
            )
            return redirect('assign-ticket')
    else:
        form = AssignTicketForm(instance=ticket)
        form.fields['engineer'].queryset = User.objects.filter(
            is_engineer=True
        )
        return render(
            request,
            'tickets/assign_ticket.html',
            {'form': form, 'ticket': ticket}
        )

@login_required
def engineer_active_tickets(request):
    if not request.user.is_engineer and not request.user.is_superuser:
        messages.error(request, "You are not allowed to view this page")
        return redirect('dashboard')
    ticket_list = Ticket.objects.filter(
        engineer=request.user,
        is_resolved=False
    ).order_by('-created_on')

    paginator = Paginator(ticket_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tickets': page_obj.object_list,
        'active_tickets': ticket_list.count(),
        'page_obj': page_obj,
    }
    return render(request, 'tickets/engineer_active_tickets.html', context)

@login_required
def resolve_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if (
    request.user != ticket.engineer and
    not request.user.is_superuser
    ):
        messages.error(request, "You are not allowed to edit this ticket.")
        return redirect('dashboard')
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs
        ticket.is_resolved = True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request, 'Ticket is now resolved and closed')
        return redirect('dashboard')

@login_required
def customer_resolved_tickets(request):
    ticket_list = Ticket.objects.filter(
        customer=request.user,
        is_resolved=True
    ).order_by('-created_on')

    paginator = Paginator(ticket_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tickets': page_obj.object_list,
        'resolved_tickets': ticket_list.count(),
        'page_obj': page_obj,
    }
    return render(request, 'tickets/customer_resolved_tickets.html', context)

@login_required
def engineer_resolved_tickets(request):
    if not request.user.is_engineer and not request.user.is_superuser:
        messages.error(request, "You are not allowed to view this page")
        return redirect('dashboard')
    ticket_list = Ticket.objects.filter(
        engineer=request.user,
        is_resolved=True
    ).order_by('-created_on')

    paginator = Paginator(ticket_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tickets': page_obj.object_list,
        'resolved_tickets': ticket_list.count(),
        'page_obj': page_obj,
    }
    return render(request, 'tickets/engineer_resolved_tickets.html', context)

@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.user != ticket.customer:
        messages.error(request, "You are not allowed to edit this ticket.")
        return redirect('dashboard')
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Your ticket has been deleted.")
        return redirect('dashboard')
    return render(
        request,
        'tickets/delete_ticket_confirm.html',
        {'tickets': ticket}
    )

@login_required
def edit_ticket_description(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.user != ticket.customer:
        messages.error(request, "You are not allowed to edit this ticket.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = EditTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket-details', ticket_id=ticket_id)
    else:
        form = EditTicketForm(instance=ticket)

    return render(
        request,
        'tickets/edit_description.html',
        {'form': form, 'ticket': ticket}
    )
