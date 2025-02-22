from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
   return HttpResponse("<h1>Welcome! You are logged in.</h1>")


@login_required
def choose_view(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'provide':
            return redirect('provide_page')
        elif choice == 'borrow':
            return redirect('borrow_page')
    return render(request, 'choose.html')