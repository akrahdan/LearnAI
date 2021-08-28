import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async
from django.http.response import Http404

from .models import Thread, ChatMessage


User = get_user_model()

class TaskConsumer(AsyncConsumer):
    async def welcome_message(self, event):
       
        timeout = event.get("timeout", 20)
        await asyncio.sleep(timeout)
        message = event.get("message")
        sender_id = event.get('sender_id')
        receiver_id = event.get('receiver_id')
        sender_user = await self.get_user_by_id(sender_id)
        receiver_user = await self.get_user_by_id(receiver_id)
        thread_obj = await self.get_thread(sender_user, receiver_user.username)
        await self.create_welcome_chat_message(thread_obj, sender_user, message)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_welcome_chat_message(self, thread, user, message):
        return ChatMessage.objects.create(thread=thread, user=user, message=message)


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # when the socket connects
        # self.kwargs.get("username")
        self.roomId = self.scope['url_route']['kwargs']['room_id']
        user = self.scope['user']
        
        thread_obj = await self.get_object(user, self.roomId)
        if user == thread_obj.first or thread_obj.second:

            self.chat_thread = thread_obj
            self.room_group_name = thread_obj.room_group_name # group

            await self.channel_layer.group_add(
                self.room_group_name, 
                self.channel_name
            )
            self.rando_user = await self.get_name()
            await self.send({
                "type": "websocket.accept"
            })


    async def websocket_receive(self, event): # websocket.receive
        message_data = json.loads(event['text'])
        #print()
        user = self.scope['user']
        username = "unknown"
        if user.is_authenticated:
            username = user.username
        message_data["user"] = username
        await self.create_chat_message(user, message_data['msg'])
        final_message_data = json.dumps(message_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': final_message_data
            }
        )

    async def broadcast_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({'msg': "Loading data please wait...", 'user': 'admin'})
        })
        await asyncio.sleep(15) ### chatbot? API -> another service --> response --> send
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })

    async def websocket_disconnect(self, event):
        # when the socket connects
        #print(event)
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )

    @database_sync_to_async
    def get_name(self):
        return User.objects.all()[0].username

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]
    
    @database_sync_to_async
    def get_object(self, roomId):
        try:
            obj = Thread.objects.get(id=roomId)
        except Thread.DoesNotExist:
            raise Http404

    @database_sync_to_async
    def create_chat_message(self, user, message):
        thread = self.chat_thread
        return ChatMessage.objects.create(thread=thread, user=user, message=message)


class ChatNewConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        room_id = 'compose'
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = self.other_username

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

        await self.send({
            "type": "websocket.send",
            "text": "Hello world"
        })
    
    async def websocket_receive(self, event):

        print(event)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': ''
            }
        )



    
    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['message']
        })
    
    async def websocket_disconnect(self, event):
        # when the socket connects
        #print(event)
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )


