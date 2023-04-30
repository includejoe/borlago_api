from rest_framework import serializers

from .models import CollectorUnit


class CollectorUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectorUnit
        fields = "__all__"
