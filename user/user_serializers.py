from rest_framework import serializers

from .models import User, Location, PaymentMethod


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "is_superuser",
            "last_login",
            "password",
            "is_staff",
            "is_deleted",
            "is_verified",
            "is_suspended",
            "updated_at",
            "collector_unit",
            "groups",
            "user_permissions",
        ]

        read_only_fields = ["id", "user_type", "email", "created_at"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["user", "created_at", "updated_at"]

        read_only_fields = ["id", "created_at"]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        exclude = ["user", "created_at"]

        read_only_fields = ["id", "created_at"]


class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["password"]

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
