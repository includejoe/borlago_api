from django.urls import re_path

from user.consumers import update_c_unit_location_asgi

websocket_urlpatterns = [
    re_path(
        r"^ws/collector-unit/live/location/$",
        update_c_unit_location_asgi,
    )
]
