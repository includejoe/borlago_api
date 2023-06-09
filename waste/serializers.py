from rest_framework import serializers

from .models import WasteCollectionRequest, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["id", "user", "status", "transaction_id"]


class WCRSerializer(serializers.ModelSerializer):
    pick_up_location = serializers.SerializerMethodField()
    collector_unit = serializers.SerializerMethodField()

    def get_pick_up_location(self, obj):
        return obj.pick_up_location.name

    def get_collector_unit(self, obj):
        if obj.collector_unit:
            return obj.collector_unit.name
        return None

    class Meta:
        model = WasteCollectionRequest
        exclude = ["user", "updated_at"]

        read_only_fields = [
            "created_at",
            "payment",
            "collector_unit",
            "price",
            "collection_datetime",
            "status",
        ]
