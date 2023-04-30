from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, ParseError

from . import serializers
from .utils import check_is_admin
from user.models import CollectorUnit


# Create your views here.
class CreateCollectorUnitAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateCollectorUnitSerializer

    def create(self, request):
        is_admin = check_is_admin(request)

        if not is_admin:
            return Response(
                {"detail": "You do not have permission to access this resource"},
                status=status.HTTP_403_FORBIDDEN,
            )

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


class GetCollectorsAPIView(generics.RetrieveAPIView):
    pass


get_collectors_view = GetCollectorsAPIView.as_view()


class GetCollectorUnitsAPIView(generics.RetrieveAPIView):
    pass


get_collector_units_view = GetCollectorUnitsAPIView.as_view()


class CollectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


collector_detail_view = CollectorDetailAPIView.as_view()


class CollectorUnitDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


collector_unit_detail_view = CollectorUnitDetailAPIView.as_view()
