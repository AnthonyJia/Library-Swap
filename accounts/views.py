from django.http import HttpResponse
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'accounts/home.html')  # Render the homepage template
