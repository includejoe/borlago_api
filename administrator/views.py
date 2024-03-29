import environ
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from . import serializers
from user.models import CollectorUnit, User
from waste.models import WasteCollectionRequest
from base.utils.validate_admin import check_is_admin

env = environ.Env()
environ.Env.read_env()


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


class AddOrRemoveCollectorToUnitAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CollectorUnitDetailSerializer

    def patch(self, request):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        admin = request.user
        collector_id = request.data.get("collector_id", None)
        unit_name = request.data.get("collector_unit", None)
        type = request.data.get("type", None)

        if collector_id is None:
            return Response(
                {"detail": "Must provide collector ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if unit_name is None:
            return Response(
                {"detail": "Must provide collector_unit"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if type is None:
            return Response(
                {"detail": "Must provide type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            unit = CollectorUnit.objects.get(name=unit_name)
            collector = User.objects.get(collector_id=collector_id)

            if collector.user_type != 3:
                return Response(
                    {"detail": "This user is not a collector"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # check if collector already belongs to this unit
            already_added = unit.collectors.filter(collector_id=collector_id).exists()

            if type == "add":
                # check if unit has more than 5 collectors
                if unit.collectors.all().count() >= int(env("MAXIMUM_COLLECTORS")):
                    return Response(
                        {
                            "detail": "This unit has reached it's maximum number of collectors"
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

                if already_added:
                    return Response(
                        {"detail": "This collector already belongs to this unit"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                else:
                    # check if collector already belongs to a unit
                    all_units = CollectorUnit.objects.all()

                    if all_units.filter(collectors=collector).exists():
                        return Response(
                            {"detail": "This collector already belongs to a unit"},
                            status=status.HTTP_403_FORBIDDEN,
                        )

                    unit.collectors.add(collector)
            elif type == "remove":
                if already_added:
                    unit.collectors.remove(collector)
                else:
                    return Response(
                        {"detail": "This collector does not belong to this unit"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST
                )

            # set updated_by field
            unit.updated_by = admin

            unit.save()
            serializer = self.serializer_class(unit)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "This collector does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except CollectorUnit.DoesNotExist:
            return Response(
                {"detail": "This collector unit does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            raise APIException(detail=e)


add_or_remove_collector_to_unit_view = AddOrRemoveCollectorToUnitAPIView.as_view()


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


class CollectorDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CollectorSerializer

    def retrieve(self, request, collector_id):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        try:
            collector = User.objects.get(id=collector_id)

            if collector.user_type != 3:
                return Response(
                    {"detail": "This user is not a collector"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.serializer_class(collector)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "This collector does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(detail=e)

    def patch(self, request, collector_id):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        data = request.data

        try:
            collector = User.objects.get(id=collector_id)
            serializer = self.serializer_class(
                collector,
                data=data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "This collector does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(detail=e)


collector_detail_view = CollectorDetailAPIView.as_view()


class CollectorUnitDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CollectorUnitDetailSerializer

    def retrieve(self, request, unit_id):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        try:
            unit = CollectorUnit.objects.get(id=unit_id)
            serializer = self.serializer_class(unit)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except CollectorUnit.DoesNotExist:
            return Response(
                {"detail": "This collector unit does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(detail=e)

    def patch(self, request, unit_id):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        admin = request.user
        data = {**request.data, "updated_by": admin.id}

        try:
            unit = CollectorUnit.objects.get(id=unit_id)
            serializer = self.serializer_class(
                unit,
                data=data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except CollectorUnit.DoesNotExist:
            return Response(
                {"detail": "This collector unit does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(detail=e)


collector_unit_detail_view = CollectorUnitDetailAPIView.as_view()


class WasteCollectionRequestsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WasteCollectionRequestSerializer
    queryset = WasteCollectionRequest.objects.all()

    def list(self, request, *args, **kwargs):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response
        return super().list(request, *args, **kwargs)


get_wcrs_view = WasteCollectionRequestsAPIView.as_view()


class WasteCollectionRequestDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WasteCollectionRequestSerializer

    def retrieve(self, request, wcr_id):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        try:
            wcr = WasteCollectionRequest.objects.get(id=wcr_id)

            serializer = self.serializer_class(wcr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "This wcr does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(detail=e)


wcr_detail_view = WasteCollectionRequestDetailAPIView.as_view()


class FilterCollectorUnitsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CollectorUnitSerializer

    def get(self, request):
        error_response = check_is_admin(request)

        if error_response is not None:
            return error_response

        name = request.query_params.get("name", None)
        unit_status = request.query_params.get("status", None)
        region = request.query_params.get("region", None)
        country = request.query_params.get("country", None)
        units = CollectorUnit.objects.all()

        if name:
            name = "".join(c.upper() if c.isalpha() else c for c in name)
            units = units.filter(name__icontains=name)
        if unit_status:
            if unit_status == "Available":
                units = units.filter(available=True)
            else:
                units = units.filter(available=False)
        if region:
            units = units.filter(region__icontains=region)
        if country:
            units = units.filter(country__icontains=country)

        serializer = self.serializer_class(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


filter_collector_units_view = FilterCollectorUnitsAPIView.as_view()
