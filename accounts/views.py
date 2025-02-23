from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'accounts/home.html')  # Render the homepage template

def anonymous_view(request):
    return render(request, 'accounts/anonymous.html')

@login_required
def choose_view(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')  # 'provider' or 'borrower'
        
        if choice == 'provider':
            # Check if the user is approved
            if request.user.is_provider_approved:
                request.user.role = 'provider'
                request.user.save()
                return redirect('provide_page')
            else:
                # Not approved
                messages.error(request, "You do not have permission to be a provider yet.")
                return redirect('choose')  # reload the same page or show a different message page
        elif choice == 'borrower':
            # They want to be a borrower
            request.user.role = 'borrower'
            request.user.save()
            return redirect('borrow_page')

    return render(request, 'accounts/choose.html')

@login_required
def provide_view(request):
    # Render a page for providers
    return render(request, 'accounts/provide.html')

@login_required
def borrow_view(request):
    # Render a page for borrowers
    return render(request, 'accounts/borrow.html')