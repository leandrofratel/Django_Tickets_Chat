import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from chatapp.models import Room, Message, User
import base64


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        room_name = text_data_json.get("room_name")
        image_data = text_data_json.get("image")  # Novo campo para imagem

        if message:
            # Se for uma mensagem de texto
            await self.save_message(message, username, room_name)
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "sendMessage",
                    "message": message,
                    "username": username,
                    "room_name": room_name,
                }
            )
        elif image_data:
            # Se for uma imagem
            image_url = await self.save_image(image_data, username, room_name)
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "sendImage",
                    "image_url": image_url,
                    "username": username,
                    "room_name": room_name,
                }
            )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))
    
    async def sendImage(self, event):
        image_url = event["image_url"]
        username = event["username"]
        await self.send(text_data=json.dumps({
            "image_url": image_url,
            "username": username
        }))
    
    @sync_to_async
    def save_message(self, message, username, room_name):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        Message.objects.create(user=user, room=room, content=message)

    @sync_to_async
    def save_image(self, image_data, username, room_name):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        
        # Decodificando a imagem
        format, imgstr = image_data.split(';base64,')  # Separando o formato base64
        ext = format.split('/')[1]  # Obtendo a extensão do arquivo
        img_data = base64.b64decode(imgstr)
        
        # Salvando a imagem no servidor
        image_name = f"{username}_{room_name}_{user.id}_image.{ext}"
        path = default_storage.save(f"chat_images/{image_name}", ContentFile(img_data))
        image_url = default_storage.url(path)
        
        # Salvando a imagem no banco de dados
        Message.objects.create(user=user, room=room, image=image_url)
        
        return image_url
