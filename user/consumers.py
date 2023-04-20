import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import CollectorUnit

from .serializers import CollectorUnitSerializer

# c_unit => CollectorUnit


class UpdateCUnitLocationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = (
            self.scope["url_route"]["kwargs"]["country"]
            + "-"
            + self.scope["url_route"]["kwargs"]["region"]
        )
        self.room_group_name = f"region/{self.room_name}"

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

    def receive(self, text_data=None, bytes_data=None):
        # parse json data into dictionary object
        text_data_json = json.loads(text_data)

        # send message to room group
        update_type = {"type": "update_location"}
        return_dict = {**update_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, return_dict)

    def update_location(self, event):
        location_data = event.copy()
        location_data.pop("type")

        c_unit_id = self.scope["url_route"]["kwargs"]["c_unit_id"]

        c_unit = CollectorUnit.objects.filter(id=c_unit_id).update(**location_data)

        serializer = CollectorUnitSerializer(c_unit)

        # Send updated data to WebSocket
        self.send(text_data=json.dumps(serializer.data))


update_c_unit_location_asgi = UpdateCUnitLocationConsumer.as_asgi()
