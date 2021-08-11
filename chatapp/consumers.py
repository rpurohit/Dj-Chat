#chatapp/consumers.py
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import Message
import json

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    '''
        This function is handling the connection between the user and the room.
    '''
    # Adding the message in database
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.get(username=author)
        message = Message.objects.create(
            author = author_user,
            content = data['message'],
            roomname = data['roomname']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    # Retriveing messages from database
    def fetch_messages(self, data):
        messages = Message.previous_messages(self, data['roomname'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_fetch(messages)
        }
        self.send_message(content)

    # Fetching the messages
    def messages_to_fetch(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    # Serializing the message
    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['commands']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))