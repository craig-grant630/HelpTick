from django.urls import path
from . import views

urlpatterns = [
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    path('customer-active-tickets/', views.customer_active_tickets, name='customer-active-tickets'),
]