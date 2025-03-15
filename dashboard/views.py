from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user  # Get the currently logged-in user
    if user.is_customer:  # Check if the user is a customer
        return render(request, 'dashboard/customer_dashboard.html')