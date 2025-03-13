from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegisterCustomerForm

User = get_user_model()

# Create your views here.

def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_vaild():
            new_user = form.save(commit=False)
            new_user.is_customer = True
            new_user.save()
            messages.success(request, "Thank you, your account has been created. Please log in")
            return redirect('login')
        else:
            messages.error(request, 'Oops... Something went wrong. Please check the form')
            return redirect('register-customer')
