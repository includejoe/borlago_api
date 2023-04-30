from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, ParseError

from . import serializers
from .utils import check_is_admin
from user.models import CollectorUnit, User


# Create your views here.
class CreateCollectorUnitAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateCollectorUnitSerializer

    def create(self, request):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        admin = request.user
        data = request.data
        data["created_by"] = admin

        unit = CollectorUnit.objects.create(**data)
        serializer = self.serializer_class(unit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


create_collector_unit_view = CreateCollectorUnitAPIView.as_view()


class AddCollectorToUnitAPIView(generics.UpdateAPIView):
    pass


add_collector_to_unit_view = AddCollectorToUnitAPIView.as_view()


class GetCollectorsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CollectorSerializer
    queryset = User.objects.filter(user_type=3)

    def list(self, request, *args, **kwargs):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response
        return super().list(request, *args, **kwargs)


get_collectors_view = GetCollectorsAPIView.as_view()


class GetCollectorUnitsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CollectorUnitSerializer
    queryset = CollectorUnit.objects.all()

    def list(self, request, *args, **kwargs):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response
        return super().list(request, *args, **kwargs)


get_collector_units_view = GetCollectorUnitsAPIView.as_view()


class CollectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


collector_detail_view = CollectorDetailAPIView.as_view()


class CollectorUnitDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


collector_unit_detail_view = CollectorUnitDetailAPIView.as_view()
