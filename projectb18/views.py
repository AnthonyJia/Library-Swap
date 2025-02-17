from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome! You are logged in.</h1>")