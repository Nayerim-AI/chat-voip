from django.urls import re_path
from .consumers import ChatConsumer, PrivateChatConsumer, CallConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),  # Global Chat
    re_path(r"ws/dm/(?P<user1>\w+)/(?P<user2>\w+)/$", PrivateChatConsumer.as_asgi()),  # Private Chat
    re_path(r"ws/call/(?P<room_name>\w+)/$", CallConsumer.as_asgi()),
]
