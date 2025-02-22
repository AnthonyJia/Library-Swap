from django.urls import path, include
from .views import home  # Import the home view

urlpatterns = [
    path('', home, name='home'),  # Default homepage
    path('accounts/', include('allauth.urls')),  # Authentication URLs under /accounts/
]