from django.http import HttpResponse
from django.shortcuts import redirect, render

def landing(request):
    # This is the final landing page for authenticated users.
    return HttpResponse("<h1>Welcome! You are logged in.</h1>")

def root_view(request):
    # If the user is authenticated, send them to the landing page.
    if request.user.is_authenticated:
        return redirect('home')
    # Otherwise, redirect to the login page.
    return redirect('/accounts/login/')