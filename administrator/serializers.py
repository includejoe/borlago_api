from rest_framework.serializers import ModelSerializer

from user.models import User, CollectorUnit


class CreateCollectorUnitSerializer(ModelSerializer):
    class Meta:
        model = CollectorUnit
        fields = ["id", "country", "name", "region", "created_by"]

        read_only_fields = ["id", "name", "created_by"]


class CollectorUnitSerializer(ModelSerializer):
    class Meta:
        model = CollectorUnit
        fields = "__all__"

        read_only_fields = ["id", "created_at", "name"]


class CollectorSerializer(ModelSerializer):
    collector_unit = CollectorUnitSerializer(many=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "gender",
            "is_staff",
            "collector_unit",
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
        ]
