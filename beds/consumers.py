import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class BedNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "bed_notifications"
        self.room_group_name = "chat_%s" % self.room_name # Channels uses group names like chat_<room-name>

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        print("WebSocket connected to group: ", self.room_group_name)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("WebSocket disconnected from group: ", self.room_group_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        # This consumer is primarily for sending notifications, not receiving from client
        pass

    # Receive message from room group
    def bed_available_notification(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
