import environ
import requests
from decimal import Decimal
from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, ParseError
from geopy.distance import distance as geopy_distance

from . import serializers
from .models import WasteCollectionRequest, Payment
from user.models import Location, CollectorUnit

env = environ.Env()
environ.Env.read_env()


# Create your views here.
class CreateWCRAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WCRSerializer

    def create(self, request):
        data = request.data
        data["user"] = request.user

        try:
            pick_up_location = data.get("pick_up_location")
            pick_up_location = Location.objects.get(id=pick_up_location)

            if pick_up_location.user != request.user:
                return Response(
                    {"detail": "This user does not own this pick_up_location"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            data["pick_up_location"] = pick_up_location
            wcr = WasteCollectionRequest.objects.create(**data)

            """ google cloud vision algorithm to identify contents of waste 
                in the waste photo and write out the price for waste is implemented
            """
            payment_amount = 3.56

            return Response(
                {"amount_to_pay": payment_amount},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            raise APIException(detail=e)


create_wcr_view = CreateWCRAPIView.as_view()


class ListUserWCRsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WCRSerializer

    def list(self, request):
        user = request.user
        try:
            wcrs = WasteCollectionRequest.objects.filter(user=user)
            serializer = self.serializer_class(wcrs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


list_user_wcrs_view = ListUserWCRsAPIView.as_view()


class WCRDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WCRSerializer

    def retrieve(self, request, wcr_id):
        user = request.user
        try:
            wcr = WasteCollectionRequest.objects.get(user=user, id=wcr_id)
            serializer = self.serializer_class(wcr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            APIException(detail=e)


wcr_detail_view = WCRDetailAPIView.as_view()


class MakeWCRPaymentAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PaymentSerializer

    # TODO:  update WCR with assigned CU, payment & status
    # TODO: return updated WCR and calculated collector distance from pickup location

    def create(self, request):
        data = request.data
        payer = request.user
        data["payer"] = payer
        wcr_id = data.get("wcr", None)

        # fields to update
        self.payment = None
        self.closest_collector_unit = None
        self.collection_datetime = None

        try:
            if wcr_id is None:
                raise ParseError(detail="Invalid Waste Collection Request ID", code=404)
            wcr = WasteCollectionRequest.objects.get(id=wcr_id)
            # reassign wcr field from id to wcr instance
            data["wcr"] = wcr
        except WasteCollectionRequest.DoesNotExist:
            raise ParseError(detail="Invalid Waste Collection Request ID", code=404)

        # if payment type is MoMo
        if data["type"] == 1:
            if payer.momo_number is None or payer.momo_number == "":
                raise ParseError(detail="User must have a momo number", code=404)

            # Send payment request to hubtel
            # response = requests.post(
            #     f"https://devp-reqsendmoney-230622-api.hubtel.com/request-money/{payer.momo_number}",
            #     json={
            #         "amount": data["amount"],
            #         "title": "BorlaGo WCR Payment",
            #         "description": "Payment for a waste collection request",
            #         "clientReference": env("HUBTEL_CLIENT_ID"),
            #         "callbackUrl": "http://example.com",
            #     },
            # )

            # if response.status_code == 201:
            #     # Payment request successful
            #     transaction_id = "Sample Transaction ID"
            #     payment = Payment.objects.create(**data, transaction_id=transaction_id)

            #     return Response(
            #         {"detail": "Payment Successful"},
            #         status=status.HTTP_201_CREATED,
            #     )
            # else:
            #     # Payment request failed
            #     print(response)
            #     return Response(
            #         {"detail": "Payment Error"},
            #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     )
        else:
            # step 1 - Find closest collector

            pick_up_location = wcr.pick_up_location
            latitude = pick_up_location.latitude
            longitude = pick_up_location.longitude
            delta = Decimal(0.018)

            collector_units = CollectorUnit.objects.filter(
                available=True,
                latitude__gte=Decimal(latitude) - delta,
                latitude__lte=Decimal(latitude) + delta,
                longitude__gte=Decimal(longitude) - delta,
                longitude__lte=Decimal(longitude) + delta,
            ).order_by("latitude", "longitude")

            self.closest_collector_unit = collector_units.first()

            if self.closest_collector_unit:
                closest_coords = (
                    self.closest_collector_unit.latitude,
                    self.closest_collector_unit.longitude,
                )
                pickup_coords = (Decimal(latitude), Decimal(longitude))
                distance = geopy_distance(closest_coords, pickup_coords).km

                return Response(
                    {"distance": distance},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"detail": "No collector units found"},
                    status=status.HTTP_404_NOT_FOUND,
                )


make_wcr_payment_view = MakeWCRPaymentAPIView.as_view()
