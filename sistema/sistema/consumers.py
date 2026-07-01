import json
import base64
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from chatapp.models import Room, Message, User
from django.db import transaction
from asgiref.sync import sync_to_async
from collections import defaultdict
import asyncio
from django.utils import timezone
from datetime import timedelta


class ChatConsumer(AsyncWebsocketConsumer):
    # Limitadores de taxa: max 10 mensagens/s, 60 mensagens/mínimo
    RATE_LIMITS = {
        'messages_per_second': 10,
        'messages_per_minute': 60,
    }

    # Trackers de limite de taxa globais (em um ambiente de produção, você pode querer usar Redis)
    rate_limiter_counters = defaultdict(lambda: {'messages_per_second': defaultdict(int), 'messages_per_minute': defaultdict(int)})

    async def clean_rate_limiters(self):
        # Limpa o registro de usuários antigo evitando assim perdas de memória
        current_time = asyncio.get_event_loop().time()
        cutoff_time = current_time - 65
        for room_group_name in list(self.rate_limiter_counters.keys()):
            for user in list(self.rate_limiter_counters[room_group_name]['messages_per_minute'].keys()):
                if self.rate_limiter_counters[room_group_name]['messages_per_minute'][user] < cutoff_time:
                    del self.rate_limiter_counters[room_group_name]['messages_per_minute'][user]

    @sync_to_async
    def get_rate_limit_status(self, room_group_name, username):
        # Retorna o status do limite de taxa para o usuário
        return {
            'messages_per_second_count': self.rate_limiter_counters[room_group_name]['messages_per_second'][username],
            'messages_per_minute_count': self.rate_limiter_counters[room_group_name]['messages_per_minute'][username],
        }

    async def connect(self):
        # Validação de autenticação do espaço de rota
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_slug']
            self.room_group_name = 'chat_%s' % self.room_name

            # Adiciona usuário ao grupo de chat
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            # Inicia a limpeza periódica do limitador de taxa
            self.rate_limit_task = asyncio.create_task(self.clean_rate_limiter_periodically())

        except KeyError:
            await self.close(code=4008, reason="Missing room path")

    async def clean_rate_limiter_periodically(self):
        # Limpa os dados do limitador a cada 5 minutos
        while True:
            await asyncio.sleep(300)
            await self.clean_rate_limiter()

    @sync_to_async
    def clean_rate_limiter(self):
        # Limpa dados do limitador antigos (mantém os últimos 60 segundos)
        cutoff_time = timezone.now(timezone.utc) - timedelta(seconds=60)
        for room_group_name in list(self.rate_limiter_counters.keys()):
            for timestamp in list(self.rate_limiter_counters[room_group_name].keys()):
                if timestamp < cutoff_time.timestamp():
                    del self.rate_limiter_counters[room_group_name][timestamp]

    async def disconnect(self, close_code):
        # Cancela a tarefa periódica
        if hasattr(self, 'rate_limit_task'):
            self.rate_limit_task.cancel()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def validate_input(self, data):
        # Validação básica do payload
        if not isinstance(data, dict):
            raise ValueError("Invalid data format")

        required_fields = ['username', 'room_name']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if 'message' in data:
            message = data['message']
            if not isinstance(message, str) or len(message) > 1000:
                raise ValueError("Invalid message format or length")
            # Suspira para spam/suspeito
            if message.count('http://') > 2 or message.lower().startswith('spam'):
                raise ValueError("Suspicious message detected")

        if 'image' in data:
            image_data = data['image']
            if not isinstance(image_data, str) or not image_data.startswith('data:image/'):
                raise ValueError("Invalid image format")
            try:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[1]
                img_data = base64.b64decode(imgstr)
                if len(img_data) > 10 * 1024 * 1024:  # Max 10MB
                    raise ValueError("Image too large")
            except Exception as e:
                raise ValueError(f"Invalid base64 image: {str(e)}")

        return True

    async def check_rate_limit(self, username):
        # Verifica o limite de taxa para o usuário
        current_time = asyncio.get_event_loop().time()
        current_minute = int(current_time / 60)

        room_group_name = self.room_group_name

        # Atualiza/reinicia o contador por segundo
        if current_time - int(self.rate_limiter_counters[room_group_name]['messages_per_second'][username]) >= 1:
            self.rate_limiter_counters[room_group_name]['messages_per_second'][username] = current_time
            self.rate_limiter_counters[room_group_name]['messages_per_second'][username] = 1
        else:
            self.rate_limiter_counters[room_group_name]['messages_per_second'][username] += 1

        # Atualiza/reinicia o contador por minuto
        if current_minute - int(self.rate_limiter_counters[room_group_name]['messages_per_minute'][username]) >= 1:
            self.rate_limiter_counters[room_group_name]['messages_per_minute'][username] = current_minute
            self.rate_limiter_counters[room_group_name]['messages_per_minute'][username] = 1
        else:
            self.rate_limiter_counters[room_group_name]['messages_per_minute'][username] += 1

        # Verifica os limites
        if self.rate_limiter_counters[room_group_name]['messages_per_second'][username] > self.RATE_LIMITS['messages_per_second']:
            raise ValueError("Too many messages per second. Please slow down.")

        if self.rate_limiter_counters[room_group_name]['messages_per_minute'][username] > self.RATE_LIMITS['messages_per_minute']:
            raise ValueError("Too many messages per minute. Please try again later.")

        return True

    async def receive(self, text_data):
        # Decodifica e valida os dados recebidos
        try:
            text_data_json = json.loads(text_data)
            await self.validate_input(text_data_json)

            if text_data_json.get("typing"):
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "typingNotification",
                        "username": text_data_json["username"],
                        "room_name": text_data_json.get("room_name", ""),
                    }
                )
                return

            await self.check_rate_limit(text_data_json['username'])
        except json.JSONDecodeError:
            await self.close(code=4007, reason="Invalid data format")
            return
        except ValueError as e:
            await self.close(code=4008, reason=str(e))
            return

        # Atualiza se houver mensagem ou imagem
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        room_name = text_data_json.get("room_name")
        image_data = text_data_json.get("image")

        # Salva a mensagem/imagem imediatamente com uma transação
        try:
            if message:
                # Validação adicional
                if len(message.strip()) == 0:
                    await self.close(code=4008, reason="Empty message")
                    return

                await self.save_message(message, username, room_name)
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "sendMessage",
                        "message": message,
                        "username": username,
                        "room_name": room_name,
                    }
                )

            elif image_data:
                # Otimiza e salva a imagem
                image_url = await self.save_optimized_image(image_data, username, room_name)
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "sendImage",
                        "image_url": image_url,
                        "username": username,
                        "room_name": room_name,
                    }
                )
        except Exception as e:
            await self.close(code=4009, reason=f"Error processing message: {str(e)}")

    async def sendMessage(self, event):
        # Simplesmente envia a mensagem com um envelope adicional
        message = event["message"]
        username = event["username"]
        room_name = event.get("room_name", "")
        timestamp = event.get("timestamp", str(timezone.now().timestamp()))

        await self.send(text_data=json.dumps({
            "type": "message",
            "message": message,
            "username": username,
            "room_name": room_name,
            "timestamp": timestamp
        }))

    async def sendImage(self, event):
        # Simplesmente envia a imagem
        image_url = event["image_url"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "type": "image",
            "image_url": image_url,
            "username": username
        }))

    async def typingNotification(self, event):
        await self.send(text_data=json.dumps({
            "typing": True,
            "username": event["username"],
            "room_name": event.get("room_name", "")
        }))

    @sync_to_async
    @transaction.atomic
    def save_message(self, message, username, room_name):
        # Salva a mensagem com tratamento de falhas
        try:
            user = User.objects.get(username=username)
            room = Room.objects.get(name=room_name)
            Message.objects.create(user=user, room=room, content=message)
        except User.DoesNotExist:
            raise ValueError(f"User '{username}' not found")
        except Room.DoesNotExist:
            raise ValueError(f"Room '{room_name}' not found")

    @sync_to_async
    @transaction.atomic
    def save_optimized_image(self, image_data, username, room_name):
        """
        Salva uma imagem otimizada no servidor e no banco de dados
        """
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)

        try:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[1]
            img_data = base64.b64decode(imgstr)

            # Otimiza a imagem
            from PIL import Image
            from io import BytesIO

            img = Image.open(BytesIO(img_data))

            # Limita o tamanho da imagem (por exemplo, 1920x1080) e Reduz a qualidade da imagem
            max_size = (1920, 1080)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Reduz drasticamente a qualidade da imagem para salvar espaço em disco no servidor
            output = BytesIO()
            if img.mode in ('RGBA', 'LA'):
                # Para imagens transparentes, mantém o PNG para preservar transparência
                if ext.lower() in ['jpg', 'jpeg', 'png']:
                    img.save(output, format='PNG', quality=70, optimize=True)
                else:
                    # Para outras extensões, usa PNG para se manter seguro
                    img.save(output, format='PNG', quality=70, optimize=True)
            else:
                # Para imagens RGB ou L, usa JPEG para compressão
                img.save(output, format='JPEG', quality=70, optimize=True)

            optimized_img_data = output.getvalue()

            # Gera nome de arquivo com um timestamp unívoco (evita sobreposições)
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            unique_id = base64.urlsafe_b64encode(os.urandom(8)).decode()  # Aumenta a unicidade do nome do arquivo
            image_name = f"{username}_{room_name}_{unique_id}_{timestamp}.{ext}"

            # Salva a imagem otimizada no armazenamento
            path = default_storage.save(f"chat_images/optimized/{ext}/{image_name}", ContentFile(optimized_img_data))
            image_url = default_storage.url(path)

            # Salva a imagem no banco de dados
            Message.objects.create(user=user, room=room, image=image_url)

            return image_url

        except Exception as e:
            # Remove a imagem de armazenamento se falhar em salvar no banco de dados
            if 'path' in locals() and default_storage.exists(path):
                default_storage.delete(path)
            raise ValueError(f"Image processing failed: {str(e)}")

    @sync_to_async
    def get_online_users(self, room_group_name):
        # Obtém a lista de usuários online no grupo de chat
        # Esta função pode ser usada para o status do usuário
        channel_ids = self.channel_layer.groupsChannels.get(room_group_name, [])
        return channel_ids
