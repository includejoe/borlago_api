import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import CollectorUnit


# c_unit => CollectorUnit


class UpdateCUnitLocationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "live-location"
        self.room_group_name = f"c_unit_{self.room_name}"

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
        c_unit_id = location_data.pop("collector_unit", None)

        if c_unit_id is not None:
            if CollectorUnit.objects.filter(id=c_unit_id).exists():
                CollectorUnit.objects.filter(id=c_unit_id).update(**location_data)
                # Send Success Response to WebSocket
                self.send(text_data=f"success: {c_unit_id} location updated")
            else:
                # Send Error Response to WebSocket
                self.send(text_data="error: Invalid Collector Unit ID")
        else:
            # Send Error Response to WebSocket
            self.send(text_data="error: collector_unit can not be null")


update_c_unit_location_asgi = UpdateCUnitLocationConsumer.as_asgi()
