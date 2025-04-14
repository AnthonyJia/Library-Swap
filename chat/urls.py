from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name="chat_view"),
    path("room/<chatroom_name>", chat_view, name = "chatroom"),
    path('<username>', get_or_create_chatroom, name = "start-chat"),
]