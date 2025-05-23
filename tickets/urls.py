from django.urls import path
from . import views

urlpatterns = [
    path(
        'create-ticket/',
        views.create_ticket,
        name='create-ticket'
    ),
    path(
        'customer-active-tickets/',
        views.customer_active_tickets,
        name='customer-active-tickets'
    ),
    path(
        'customer-resolved-tickets/',
        views.customer_resolved_tickets,
        name='customer-resolved-tickets'
    ),

    path(
        'engineer-active-tickets/',
        views.engineer_active_tickets,
        name='engineer-active-tickets'
    ),
    path(
        'engineer-resolved-tickets/',
        views.engineer_resolved_tickets,
        name='engineer-resolved-tickets'
    ),

    path(
        'ticket-details/<str:ticket_id>/',
        views.ticket_details,
        name='ticket-details'
    ),
    path(
        'ticket-queue/',
        views.ticket_queue,
        name='ticket-queue'
    ),
    path(
        'assign-ticket/<str:ticket_id>/',
        views.assign_ticket,
        name='assign-ticket'
    ),
    path(
        'resolve-ticket/<str:ticket_id>/',
        views.resolve_ticket,
        name='resolve-ticket'
    ),
    path(
        'tickets/<str:ticket_id>/edit-description/',
        views.edit_ticket_description,
        name='edit-ticket-description'
    ),
    path(
        'tickets/delete/<str:ticket_id>/',
        views.delete_ticket,
        name='delete-ticket'
    ),
]
