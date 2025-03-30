from django.urls import path
from .views import chat_view

app_name = 'chat'  # Namespace for URL resolution

urlpatterns = [
    path('', chat_view, name="chat_view")
]