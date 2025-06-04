from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"


class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)  # Nama chat room (misalnya: "global")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # User yang mengirim pesan
    message = models.TextField()  # Isi pesan
    timestamp = models.DateTimeField(auto_now_add=True)  # Waktu pesan dibuat

    def __str__(self):
        return f"{self.sender.username}: {self.message} ({self.timestamp})"