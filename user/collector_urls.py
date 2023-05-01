from django.urls import path
from .views import confirm_waste_collection_view

app_name = "collector"

urlpatterns = [
    path(
        "confirm/waste-collection/",
        confirm_waste_collection_view,
        name="confirm-waste-collection",
    ),
]
