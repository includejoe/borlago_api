from rest_framework.serializers import ModelSerializer

from user.models import User, CollectorUnit, Location
from waste.models import WasteCollectionRequest


class CreateCollectorUnitSerializer(ModelSerializer):
    class Meta:
        model = CollectorUnit
        fields = ["id", "country", "name", "region", "available", "created_by"]

        read_only_fields = ["id", "name", "created_by"]


class CollectorUnitSerializer(ModelSerializer):
    class Meta:
        model = CollectorUnit
        fields = [
            "id",
            "name",
            "country",
            "region",
            "latitude",
            "longitude",
            "available",
        ]

        read_only_fields = ["id", "created_at", "name"]


class CollectorUnitNameSerializer(ModelSerializer):
    class Meta:
        model = CollectorUnit
        fields = ["name"]


class CollectorSerializer(ModelSerializer):
    collector_unit = CollectorUnitNameSerializer(many=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "gender",
            "collector_unit",
            "profile_photo",
            "is_deleted",
            "is_verified",
            "is_suspended",
        ]

        read_only_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "gender",
            "profile_photo",
        ]


class CollectorUnitDetailSerializer(ModelSerializer):
    collectors = CollectorSerializer(many=True)

    class Meta:
        model = CollectorUnit
        fields = "__all__"

        read_only_fields = ["id", "created_at", "name", "collectors"]


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ["address"]


class WasteCollectionRequestSerializer(ModelSerializer):
    pick_up_location = LocationSerializer(many=False)

    class Meta:
        model = WasteCollectionRequest
        fields = "__all__"
