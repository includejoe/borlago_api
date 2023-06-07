from rest_framework import serializers

from waste.models import WasteCollectionRequest


class ConfirmWasteCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCollectionRequest
        fields = ["id", "status", "collection_datetime"]
