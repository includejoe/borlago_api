from rest_framework import serializers

from .models import WasteCollectionRequest, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["id", "payer", "status", "transaction_id"]


class WCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCollectionRequest
        exclude = ["id"]

        read_only_fields = [
            "created_at",
            "payment",
            "collector_unit",
            "collection_datetime",
            "status",
        ]
