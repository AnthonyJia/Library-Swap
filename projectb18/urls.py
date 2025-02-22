from django.contrib import admin
from django.urls import path, include
from projectb18.views import landing, root_view

urlpatterns = [
    # The landing page for authenticated users
    path('home/', landing, name='home'),

    # Route all authentication URLs to the accounts app
    path('accounts/', include('accounts.urls')),  

    # Admin URLs
    path('admin/', admin.site.urls),

    # The root URL
    path('', root_view, name='root'),
]
