# # from channels.generic.websocket import AsyncWebsocketConsumer
# # from django.contrib.auth.models import User
# # from .models import Message
# # import json
# # from channels.db import database_sync_to_async


# # class ChatConsumer(AsyncWebsocketConsumer):
# #     print('hello')

# #     async def connect(self):
# #         self.user = self.scope["user"]
# #         self.room_name = self.user.username  # Use the username as the chat room name
# #         self.room_group_name = f'chat_{self.room_name}'

# #         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
# #         await self.accept()

# #     async def send_user_list(self):
# #         users = User.objects.exclude(username=self.user.username)
# #         user_list = [{'username': user.username} for user in users]

# #         await self.send(text_data=json.dumps({'user_list': user_list}))

# #     async def disconnect(self, close_code):
# #         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

# #     @database_sync_to_async
# #     def get_receiver(self, receiver_username):
# #         try:
# #             receiver = User.objects.get(username=receiver_username)
# #             return receiver
# #         except User.DoesNotExist:
# #             return None

# #     async def receive(self, text_data):
# #         print(text_data)
# #         message = text_data.strip()
# #         print(message)
# #         receiver_username, content = message.split(':', 1)
# #         print(receiver_username, content)

# #         receiver = await self.get_receiver(receiver_username)

# #         if not receiver:
# #             await self.send_error_message(f"User '{receiver_username}' does not exist.")
# #             return

# #         if receiver == self.user:
# #             await self.send_error_message("You cannot send a message to yourself.")
# #             return

# #         message = await self.create_message(self.user, receiver, content)
# #         await self.channel_layer.group_send(
# #             self.room_group_name,
# #             {
# #                 'type': 'chat_message',
# #                 'sender': self.user.username,
# #                 'receiver': receiver.username,
# #                 'content': content,
# #                 'timestamp': str(message.timestamp),
# #             }
# #         )
# #     @database_sync_to_async
# #     def create_message(self, sender, receiver, content):
# #         return Message.objects.create(sender=sender, receiver=receiver, content=content)    

# #     async def chat_message(self, event):
# #         await self.send(text_data=event['content'])

# #     async def send_error_message(self, error_message):
# #         await self.send(text_data=f'Error: {error_message}')



# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.contrib.auth.models import User
# from .models import Message
# import json
# from channels.db import database_sync_to_async


# class ChatConsumer(AsyncWebsocketConsumer):
#     print('hello')

#     async def connect(self):
#         self.user = self.scope["user"]
#         self.room_name = self.user.username  # Use the username as the chat room name
#         self.room_group_name = f'chat_{self.room_name}'

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def send_user_list(self):
#         users = User.objects.exclude(username=self.user.username)
#         user_list = [{'username': user.username} for user in users]

#         await self.send(text_data=json.dumps({'user_list': user_list}))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     @database_sync_to_async
#     def get_receiver(self, receiver_username):
#         try:
#             receiver = User.objects.get(username=receiver_username)
#             return receiver
#         except User.DoesNotExist:
#             return None

#     async def receive(self, text_data):
#         print(text_data)
#         message = text_data.strip()
#         print(message)
#         receiver_username, content = message.split(':', 1)
#         print(receiver_username, content)

#         receiver = await self.get_receiver(receiver_username)

#         if not receiver:
#             await self.send_error_message(f"User '{receiver_username}' does not exist.")
#             return

#         if receiver == self.user:
#             await self.send_error_message("You cannot send a message to yourself.")
#             return

#         message = await self.create_message(self.user, receiver, content)
#         sender_room_name = f'chat_{self.user.username}'
#         receiver_room_name = f'chat_{receiver_username}'

#         await self.channel_layer.group_send(
#             sender_room_name,
#             {
#                 'type': 'chat_message',
#                 'sender': self.user.username,
#                 'receiver': receiver_username,
#                 'content': content,
#                 'timestamp': str(message.timestamp),
#             }
#         )

#         await self.channel_layer.group_send(
#             receiver_room_name,
#             {
#                 'type': 'chat_message',
#                 'sender': self.user.username,
#                 'receiver': receiver_username,
#                 'content': content,
#                 'timestamp': str(message.timestamp),
#             }
#         )

#     @database_sync_to_async
#     def create_message(self, sender, receiver, content):
#         return Message.objects.create(sender=sender, receiver=receiver, content=content)

#     async def chat_message(self, event):
#         await self.send(text_data=event['content'])

#     async def send_error_message(self, error_message):
#         await self.send(text_data=f'Error: {error_message}')


from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
import json
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    print('hello')

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.user.username  # Use the username as the chat room name
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def send_user_list(self):
        users = User.objects.exclude(username=self.user.username)
        user_list = [{'username': user.username} for user in users]

        await self.send(text_data=json.dumps({'user_list': user_list}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def get_receiver(self, receiver_username):
        try:
            receiver = User.objects.get(username=receiver_username)
            return receiver
        except User.DoesNotExist:
            return None

    async def receive(self, text_data):
        print(text_data)
        message = text_data.strip()
        print(message)
        receiver_username, content = message.split(':', 1)
        print(receiver_username, content)

        receiver = await self.get_receiver(receiver_username)

        if not receiver:
            await self.send_error_message(f"User '{receiver_username}' does not exist.")
            return

        if receiver == self.user:
            await self.send_error_message("You cannot send a message to yourself.")
            return

        message = await self.create_message(self.user, receiver, content)
        sender_room_name = f'chat_{self.user.username}'
        receiver_room_name = f'chat_{receiver_username}'

        await self.channel_layer.group_send(
            sender_room_name,
            {
                'type': 'chat_message',
                'sender': self.user.username,
                'receiver': receiver_username,
                'content': content,
                'timestamp': str(message.timestamp),
            }
        )

        await self.channel_layer.group_send(
            receiver_room_name,
            {
                'type': 'chat_message',
                'sender': self.user.username,
                'receiver': receiver_username,
                'content': content,
                'timestamp': str(message.timestamp),
            }
        )

    @database_sync_to_async
    def create_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    async def chat_message(self, event):
        sender = event['sender']
        receiver = event['receiver']
        content = event['content']
        timestamp = event['timestamp']

        message = f"{sender} -> {receiver}: {content} ({timestamp})"

        # Send the formatted message to the client
        await self.send(text_data=message)

    async def send_error_message(self, error_message):
        await self.send(text_data=f'Error: {error_message}')
