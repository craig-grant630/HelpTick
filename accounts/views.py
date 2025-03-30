from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import RegisterCustomerForm

User = get_user_model()

# user login logout and register were helped using djangos documentation: https://docs.djangoproject.com/en/5.1/topics/auth/default/

def register_customer(request):
    if request.method == 'POST': # Posting the form
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False) # save the form but do not push the changes
            new_user.is_customer = True # Change users is_customer to true
            new_user.username = new_user.email # Make sure the email is the username
            new_user.save()
            messages.success(request, "Thank you, your account has been created. Please log in")
            return redirect('login')
        else:
            messages.error(request, 'Oops... Something went wrong. Please check the form again')
            return redirect('register-customer')
    else: # Getting the form
        form = RegisterCustomerForm()
        return render(request, 'accounts/register-customer.html', {'form':form} )

def login_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Somthing went wrong. Please check the form again")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout_customer(request):
    logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect('login')
