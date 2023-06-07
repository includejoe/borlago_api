from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from . import collector_serializers as serializers
from waste.models import WasteCollectionRequest
from base.utils.validate_collector import check_is_collector


class ConfirmWasteCollectionAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ConfirmWasteCollectionSerializer

    def patch(self, request):
        error_response = check_is_collector(request)

        if error_response is not None:
            return error_response

        data = request.data
        wcr_id = request.data["id"]

        try:
            wcr = WasteCollectionRequest.objects.get(id=wcr_id)

            if wcr.status == 3:
                return Response(
                    {"detail": "This WCR has already been completed"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.serializer_class(
                wcr,
                data=data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except WasteCollectionRequest.DoesNotExist:
            return Response(
                {"detail": "This WCR does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            raise APIException(detail=e)


confirm_waste_collection_view = ConfirmWasteCollectionAPIView.as_view()
