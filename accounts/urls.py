from django.urls import path, include
from .views import home  # Import the home view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import choose_view, provide_view, borrow_view, anonymous_view

urlpatterns = [
    path('', home, name='home'),  # Default homepage
    path('anonymous/', anonymous_view, name='anonymous'),
    path('accounts/', include('allauth.urls')),  # Authentication URLs under /accounts/
    path('choose/', choose_view, name='choose'),
    path('provide/', provide_view, name='provide_page'),
    path('borrow/', borrow_view, name='borrow_page'),
    path('logout/', LogoutView.as_view(), name='account_logout')
]