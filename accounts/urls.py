from django.urls import path, include

urlpatterns = [
    path('', include('allauth.urls')),  # Includes login, logout, and registration URLs
]
