from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import ChatMessage, Message
from django.contrib.auth.models import User

# 🔹 Global Chat View
def chat_view(request, room_name):
    users = User.objects.exclude(username=request.user.username)  # Ambil semua user kecuali yang login
    return render(request, "test_chat.html", {"room_name": room_name, "users": users})

# 🔹 Private Chat View (DM)
def private_chat_view(request, user1, user2):
    return render(request, "test_dm.html", {"user1": user1, "user2": user2})

def call_view(request):
    return render(request, "call.html")

def chat_view(request, room_name):
    messages = ChatMessage.objects.filter(room_name=room_name).order_by("timestamp")# Ambil pesan lama
    return render(request, "test_chat.html", {"room_name": room_name, "messages": messages})

# 🔹 Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect ke halaman login setelah sukses
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# 🔹 Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session["username"] = user.username
            return redirect('chat', room_name="global")  # Redirect ke global chat setelah login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 🔹 Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect ke login setelah logout
