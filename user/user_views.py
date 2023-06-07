from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password

from . import user_serializers as serializers
from .models import User, Location, PaymentMethod


# Create your views here.
class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def retrieve(self, _, email):
        try:
            user = User.objects.get(email=email)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "This user does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            raise APIException(detail=e)

    def patch(self, request, email):
        user = request.user
        data = request.data

        try:
            user_to_update = User.objects.get(email=email)

            if user.id != user_to_update.id:
                return Response(
                    {"detail": "You can not update another user's details"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.serializer_class(
                user_to_update, data=data, partial=True, context={"request": request}
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "This user does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(e)
            raise APIException(detail=e)


user_detail_view = UserDetailAPIView.as_view()


class CreateLocationAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LocationSerializer

    def create(self, request):
        user = request.user
        data = request.data
        data["user"] = user

        try:
            location = Location.objects.create(**data)
            serializer = self.serializer_class(location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise APIException(detail=e)


create_location_view = CreateLocationAPIView.as_view()


class ListLocationsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LocationSerializer

    def list(self, request):
        user = request.user
        try:
            locations = Location.objects.filter(user=user)
            serializer = self.serializer_class(locations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


list_locations_view = ListLocationsAPIView.as_view()


class LocationDetailAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LocationSerializer

    def retrieve(self, request, location_id):
        user = request.user
        try:
            location = Location.objects.get(user=user, id=location_id)
            serializer = self.serializer_class(location)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            APIException(detail=e)

    def destroy(self, request, location_id):
        user = request.user
        try:
            location = Location.objects.get(user=user, id=location_id)
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            APIException(detail=e)


location_detail_view = LocationDetailAPIView.as_view()


class CreatePaymentMethodAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PaymentMethodSerializer

    def create(self, request):
        user = request.user
        data = request.data
        data["user"] = user

        try:
            payment_method = PaymentMethod.objects.create(**data)
            serializer = self.serializer_class(payment_method)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise APIException(detail=e)


create_payment_method_view = CreatePaymentMethodAPIView.as_view()


class ListPaymentMethods(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PaymentMethodSerializer

    def list(self, request):
        user = request.user
        try:
            payment_methods = PaymentMethod.objects.filter(user=user)
            serializer = self.serializer_class(payment_methods, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=e)


list_payment_methods_view = ListPaymentMethods.as_view()


class PaymentMethodDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PaymentMethodSerializer

    def retrieve(self, request, method_id):
        user = request.user
        try:
            method = PaymentMethod.objects.get(user=user, id=method_id)
            serializer = self.serializer_class(method)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            APIException(detail=e)

    def destroy(self, request, method_id):
        user = request.user
        try:
            method = PaymentMethod.objects.get(user=user, id=method_id)
            method.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            APIException(detail=e)


payment_method_detail_view = PaymentMethodDetailAPIView.as_view()


class ChangePasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PasswordSerializer

    def patch(self, request):
        user = request.user

        current_password = request.data.get("current_password", None)
        new_password = request.data.get("new_password", None)

        try:
            if check_password(new_password, user.password):
                return Response(
                    {"detail": "New password can not be same as current password"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if check_password(current_password, user.password):
                serializer = self.serializer_class(
                    user,
                    data={"password": new_password},
                    partial=True,
                    context={"request": request},
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(
                    {"detail": "Password changed successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Current password is incorrect"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Exception as e:
            raise APIException(detail=e)


change_password_view = ChangePasswordAPIView.as_view()


class ForgottenPasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PasswordSerializer


forgotten_password_view = ForgottenPasswordAPIView.as_view()
