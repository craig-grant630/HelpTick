from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user  # Get the currently logged-in user
    if user.is_customer:  # Check if the user is a customer
        return render(request, 'dashboard/customer_dashboard.html')
    elif request.user.is_engineer:
        return render(request, 'dashboard/engineer_dashboard.html')
    elif user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html')