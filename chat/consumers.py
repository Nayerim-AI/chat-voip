import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import ChatMessage

# 🔹 Global Chat Consumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = self.scope["user"].username  # Ambil username dari session
        room_name = self.room_name

        # Simpan pesan ke database dengan `ChatMessage`
        chat_message = ChatMessage.objects.create(
            sender=self.scope["user"],
            message=message,
            room_name=room_name
        )

        # Kirim pesan ke WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "timestamp": chat_message.timestamp.strftime("%H:%M")
            }
        )

# 🔹 Private Chat Consumer (DM)
class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user1 = self.scope["url_route"]["kwargs"]["user1"]
        self.user2 = self.scope["url_route"]["kwargs"]["user2"]
        self.room_group_name = f"chat_{'_'.join(sorted([self.user1, self.user2]))}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender = data["sender"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"call_{self.room_name}"

        # Gabung ke room WebRTC signaling
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Keluar dari room WebRTC signaling
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        # Broadcast ke semua user di room kecuali sender
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "webrtc_signal",
                "message": data,
            }
        )

    async def webrtc_signal(self, event):
        await self.send(text_data=json.dumps(event["message"]))
