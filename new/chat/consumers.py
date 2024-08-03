import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from myaccount.models import Account
from chat.models import UserBlock
from .models import Conversation, PrivateMessage
from asgiref.sync import sync_to_async
from django.db.models import Prefetch, Q
 
chat_consumers = {} 

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        if isinstance(self.user, AnonymousUser):
            await self.close()
        else:
            self.room_group_name = f'user_{self.user.id}'
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.set_user_connected(self.user, True)
            chat_consumers[self.user.id] = self
            print(chat_consumers[self.user.id])
            await self.accept()

    async def disconnect(self, close_code):
        if not isinstance(self.user, AnonymousUser):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.set_user_connected(self.user, False)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        
        if 'message' in text_data_json and 'issuer' in text_data_json and 'receiver' in text_data_json:
            message = text_data_json['message']
            issuer_username = text_data_json['issuer']
            receiver_username = text_data_json['receiver']

            if isinstance(self.user, AnonymousUser):
                return
            
            try:
                issuer = await sync_to_async(Account.objects.get)(username=issuer_username)
                receiver = await sync_to_async(Account.objects.get)(username=receiver_username)
            except Account.DoesNotExist:
                return
            
            if receiver.id == issuer.id:
                return
            
            try:
                user_block = await sync_to_async(UserBlock.objects.get)(
                    blocker=receiver,
                    blocked=issuer
                )
                print('User blocked')
                return
            except UserBlock.DoesNotExist:
                pass

            try:
                conversation = await sync_to_async(Conversation.objects.get)(
                    Q(user1=issuer, user2=receiver) | Q(user1=receiver, user2=issuer)
                )
            except Conversation.DoesNotExist:
                conversation = await sync_to_async(Conversation.objects.create)(
                    user1=issuer,
                    user2=receiver
                )
            except Conversation.MultipleObjectsReturned:
                conversation = Conversation.objects.filter(
                    Q(user1=issuer, user2=receiver) | Q(user1=receiver, user2=issuer)
                ).first()

            try:
                private_message = await sync_to_async(PrivateMessage.objects.create)(
                    conversation=conversation,
                    message=message,
                    issuer=issuer,
                    receiver=receiver
                )
            except Exception as e:

                print(e)
                return

            await self.channel_layer.group_send(
                f'user_{receiver.id}',
                {
                    'type': 'chat_message',
                    'conversation_id': conversation.id,
                    'message': message,
                    'issuer': issuer_username,
                    'receiver': receiver_username
                }
            )
            await self.channel_layer.group_send(
                f'user_{issuer.id}',
                {
                    'type': 'chat_message',
                    'conversation_id': conversation.id,
                    'message': message,
                    'issuer': issuer_username,
                    'receiver': receiver_username
                }
            )

    async def chat_message(self, event):
        conversation_id = event['conversation_id']
        message = event['message']
        issuer = event['issuer']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'conversation_id': conversation_id,
            'message': message,
            'issuer': issuer,
            'receiver': receiver
        }))

    async def invite(self, event):
        issuer = event['issuer']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'message': 'invite',
            'issuer': issuer,
            'receiver': receiver
        }))

    @database_sync_to_async
    def set_user_connected(self, user, is_connected):
        user.is_connected = is_connected
        user.save()