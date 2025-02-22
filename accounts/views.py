from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'accounts/home.html')  # Render the homepage template

@login_required
def choose_view(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        request.user.role = choice
        request.user.save()
        if choice == 'provider':
            return redirect('provide_page')
        elif choice == 'borrower':
            return redirect('borrow_page')
    return render(request, 'choose.html')

@login_required
def provide_view(request):
    # Render a page for providers
    return render(request, 'provide.html')

@login_required
def borrow_view(request):
    # Render a page for borrowers
    return render(request, 'borrow.html')