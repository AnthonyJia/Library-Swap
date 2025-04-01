from django.urls import path
from .views import *

app_name = 'chat'  # Namespace for URL resolution

urlpatterns = [
    path('', chat_view, name="chat_view"),
    path('chat/<username>', get_or_create_chatroom, name = "start-chat"),
    path("chat/room/<chatroom_name>", chat_view, name = "chatroom"),
]