"""
URL configuration for projectb18 project.


The `urlpatterns` list routes URLs to views. For more information please see:
   https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
   1. Add an import:  from my_app import views
   2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
   1. Add an import:  from other_app.views import Home
   2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
   1. Import the include() function: from django.urls import include, path
   2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from projectb18.views import home  # Import the home view
from .views import choose_view
from allauth.account.views import LoginView


urlpatterns = [
   path('admin/', admin.site.urls),
   path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'), name='account_login'),
   path('', include('accounts.urls')),
   #path('accounts/', include('allauth.urls')),
   #path('choose/', choose_view, name='choose'),
]
