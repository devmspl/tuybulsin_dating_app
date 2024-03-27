# import base64
# import json
# import secrets
# from datetime import datetime

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# from django.core.files.base import ContentFile

# from user_management.models import CustomUser
# from .models import Message, Conversation
# from .serializers import MessageSerializer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         print("here")
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data=None, bytes_data=None):
#         # parse the json data into dictionary object
#         text_data_json = json.loads(text_data)

#         # Send message to room group
#         chat_type = {"type": "chat_message"}
#         return_dict = {**chat_type, **text_data_json}
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             return_dict,
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         text_data_json = event.copy()
#         text_data_json.pop("type")
#         message, attachment = (
#             text_data_json["message"],
#             text_data_json.get("attachment"),
#         )

#         conversation = Conversation.objects.get(id=int(self.room_name))
#         if self.scope['user'].is_authenticated:
#             user_id = self.scope['user'].id
#             sender = CustomUser.objects.get(id=user_id)

#             print('sender',sender)

#             # Attachment
#             if attachment:
#                 file_str, file_ext = attachment["data"], attachment["format"]

#                 file_data = ContentFile(
#                     base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
#                 )
#                 _message = Message.objects.create(
#                     sender=sender,
#                     attachment=file_data,
#                     text=message,
#                     conversation_id=conversation,
#                 )
#             else:
#                 _message = Message.objects.create(
#                     sender=sender,
#                     text=message,
#                     conversation_id=conversation,
#                 )
#             serializer = MessageSerializer(instance=_message)
#             # Send message to WebSocket
#             self.send(
#                 text_data=json.dumps(
#                     serializer.data
#                 )
#             )
# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         auth_token = self.scope.get('headers', {}).get('authorization')
#         print('auth_token',auth_token)
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Message



class ChatConsumer(AsyncWebsocketConsumer):
    groups = ["general"]
  
    # async def connect(self):
    #     await self.accept()
        
    #     if self.scope["user"] is not AnonymousUser:
    #         self.user_id = self.scope["user"].id
    #         messages = await self.get_messages()
    #         for message in messages:
    #             await self.send(text_data=json.dumps({
    #                 'message': message['content'],
                    
    #             }))
    #         await self.channel_layer.group_add(f"{self.user_id}-message", self.channel_name)

    # async def send_info_to_user_group(self, event):
    #     message = event["text"]
    #     await self.send(text_data=json.dumps(message))

    # async def send_last_message(self, event):
    #     last_msg = await self.get_last_message(self.user_id)
    #     last_msg["status"] = event["text"]
    #     await self.send(text_data=json.dumps(last_msg))

    # @database_sync_to_async
    # def get_last_message(self, user_id):
    #     message = Message.objects.filter(user_id=user_id).last()
    #     return message.message
    # @database_sync_to_async
    # def get_messages(self):
    #     messages = Message.objects.all()
    #     return [{'content': message.message} for message in messages]
    async def connect(self):
        await self.accept()
        
        if self.scope["user"] is not AnonymousUser:
            self.user_id = self.scope["user"].id
            self.group_name = f"chat_{self.user_id}"
            messages = await self.get_messages()
            for message in messages:
                 await self.send(text_data=json.dumps({
                     'message': message['content'],
                     'timestamp': message['timestamp']
                    
                 }))
    #         await self.channel_layer.group_add(f"{self.user_id}-message", self.channel_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_info_to_user_group(self, event):
        message = event["text"]
        await self.send(text_data=json.dumps(message))

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'timestamp': event['timestamp'],
            'sender_id': event['sender_id'],
            'recipient_id': event['recipient_id'],
        }))

    async def send_last_message(self, event):
        last_msg = await self.get_last_message(self.user_id)
        last_msg["status"] = event["text"]
        await self.send(text_data=json.dumps(last_msg))
    
    @database_sync_to_async
    def get_last_message(self, user_id):
        message = Message.objects.filter(user_id=user_id).last()
        return message.message

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, message):
        sender = User.objects.get(id=sender_id)
        recipient = User.objects.get(id=recipient_id)
        new_message = Message(sender=sender, recipient=recipient, message=message)
        new_message.save()
    @database_sync_to_async
    def get_messages(self):
        messages = Message.objects.all()
        return [{'content': message.message,'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for message in messages]