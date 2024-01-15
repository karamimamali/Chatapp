import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from urllib.parse import unquote
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def fetch_messages(self, data):
        messages = Message.last_15_messages()
        content = {
            'messages': self.messages_to_json(messages)
        }
        self.echo_last_messages(content)


    def new_message(self, data):
        content = data['message']
        author = data['from']
        author_user = User.objects.filter(username=author)[0]

        message = Message.objects.create(author=author_user, content=content)

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }

        return self.echo_content_back(content)


    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
    }

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)
        

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(message_to_json(message))

        return result

    def message_to_json(self, message):
        return {
            "author": message.author.username,
            "content": message.content,
            "timestamp": str(message.timestamp),
        }
    

    def echo_content_back(self, content):
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "echo_back", "content": content})

    def echo_back(self, event):
        content = event["content"]
        self.send(text_data=json.dumps(content))

    def echo_last_messages(self, content):
        self.send(text_data=json.dumps(content))


