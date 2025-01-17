import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'public_room'
        self.room_group_name = self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        json_text = json.loads(text_data)
        message = json_text["message"]
        username = json_text["username"] if "username" in json_text else ""  # Извлечение имени пользователя, если оно присутствует
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username  # Передача имени пользователя вместе с сообщением
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username'] if 'username' in event else ''  # Извлечение имени пользователя, если оно присутствует
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "username": username}))  # Отправка имени пользователя вместе с сообщением
