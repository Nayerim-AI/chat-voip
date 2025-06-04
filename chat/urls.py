from django.urls import path
from .views import chat_view, private_chat_view, call_view, register_view, login_view, logout_view

urlpatterns = [
    path("chat/<str:room_name>/", chat_view, name="chat"),  # Global Chat
    path("dm/<str:user1>/<str:user2>/", private_chat_view, name="private_chat_page"),  # Private Chat
    path("call/", call_view, name="call_page"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
