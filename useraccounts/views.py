from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def provider_dashboard(request):
    return render(request, 'accounts/provider_dashboard.html')

@login_required
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')

@login_required
def dashboard_router(request):
    if request.user.user_type == 'provider':
        return redirect('provider_dashboard')
    else:
        return redirect('customer_dashboard')