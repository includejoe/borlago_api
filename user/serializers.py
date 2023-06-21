from rest_framework import serializers
from django.contrib.auth import authenticate

from base.utils.validate_email import is_email_valid
from waste.models import WasteCollectionRequest
from .models import User, Location, PaymentMethod


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=128, write_only=True)
    last_name = serializers.CharField(max_length=128, write_only=True)
    country = serializers.CharField(max_length=64, write_only=True)
    gender = serializers.CharField(max_length=12, write_only=True)
    phone = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    user_type = serializers.IntegerField(write_only=True)
    jwt = serializers.SerializerMethodField()

    def get_jwt(self, obj):
        user = User.objects.get(email=obj.email)
        return user.tokens["access"]

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "country",
            "password",
            "phone",
            "gender",
            "jwt",
            "user_type",
        ]

        read_only_fields = ["collector_id"]

    def validate_email(self, value):
        valid, error_message = is_email_valid(value)
        if not valid:
            raise serializers.ValidationError(error_message)

        try:
            email_name, domain = value.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            value = "@".join([email_name, domain.lower()])

        return value

    def validate(self, data):
        gender = data.get("gender", None)
        phone = data.get("phone", None)
        user_type = data.get("user_type", None)

        if gender is None:
            raise serializers.ValidationError("gender is required")

        if phone is None:
            raise serializers.ValidationError("phone is required")

        if user_type is None:
            raise serializers.ValidationError("user_type is required")

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    user_type = serializers.IntegerField(write_only=True)
    jwt = serializers.SerializerMethodField()

    def get_jwt(self, obj):
        user = User.objects.get(email=obj.email)
        return user.tokens["access"]

    class Meta:
        model = User
        fields = ["email", "user_type", "password", "jwt"]

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email is required")

        if password is None:
            raise serializers.ValidationError("A password is required")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if user.is_deleted:
            raise serializers.ValidationError("This user account has been deleted")

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "is_superuser",
            "last_login",
            "password",
            "forgot_password_code",
            "forgot_password_code_expires_at",
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


class ConfirmWasteCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCollectionRequest
        fields = ["id", "status", "collection_datetime"]
