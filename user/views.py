from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password

from base.utils.validate_collector import check_is_collector
from waste.models import WasteCollectionRequest
from .celery_tasks import send_reset_password_email_task
from . import serializers
from .models import User, Location, PaymentMethod


# Create your views here.
class RegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        user = request.data
        try:
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise APIException(detail=e)


register_user_view = RegistrationAPIView.as_view()


class LoginAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        request_body = request.data
        user_type = request_body.get("user_type", None)
        email = request_body["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user_type == 1:
            if user.user_type != 1:
                return Response(
                    {"detail": "This user is not an administrator"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        elif user_type == 2:
            if user.user_type != 2:
                return Response(
                    {"detail": "This user is not a normal user"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        elif user_type == 3:
            if user.user_type != 3:
                return Response(
                    {"detail": "This user is not a collector"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = self.serializer_class(data=request_body)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


login_user_view = LoginAPIView.as_view()


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
            raise APIException(detail=e)


user_detail_view = UserDetailAPIView.as_view()


class AddLocationAPIView(generics.CreateAPIView):
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


add_location_view = AddLocationAPIView.as_view()


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


class DeleteLocationAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LocationSerializer

    def destroy(self, request, location_id):
        user = request.user
        try:
            location = Location.objects.get(user=user, id=location_id)
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            APIException(detail=e)


delete_location_view = DeleteLocationAPIView.as_view()


class AddPaymentMethodAPIView(generics.CreateAPIView):
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


add_payment_method_view = AddPaymentMethodAPIView.as_view()


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

    def patch(self, request, method_id):
        user = request.user
        try:
            method = PaymentMethod.objects.get(user=user, id=method_id)
            serializer = self.serializer_class(method, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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


class ChangePasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        current_password = request.data.get("current_password", None)
        new_password = request.data.get("new_password", None)

        try:
            # check if new password is same as old password
            if check_password(new_password, user.password):
                return Response(
                    {"detail": "New password can not be same as current password"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # check if current password is correct
            if check_password(current_password, user.password):
                # Update user password
                user.set_password(new_password)
                user.save()

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


class ForgotPasswordAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email", None)

        if email is None:
            return Response(
                {"detail": "Email can not be null"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
            # Generate random code
            code = get_random_string(length=6)
            user.forgot_password_code = code
            user.forgot_password_code_expires_at = timezone.now() + timezone.timedelta(
                minutes=3
            )
            user.save()
            send_reset_password_email_task.delay(user.email, user.forgot_password_code)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return APIException(detail=e)


forgot_password_view = ForgotPasswordAPIView.as_view()


class ResetPasswordAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]

    def create(self, request):
        reset_code = request.data.get("reset_code", None)
        new_password = request.data.get("new_password", None)

        if reset_code is None or new_password is None:
            return Response(
                {"detail": "reset_code or new_password can not be null"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.filter(forgot_password_code=reset_code).first()
            if user.forgot_password_code_expires_at >= timezone.now():
                # check if new password is same as old password
                if check_password(new_password, user.password):
                    return Response(
                        {"detail": "New password can not be same as current password"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                # Update user password
                user.set_password(new_password)
                user.save()

                # clear forgot_password_code and code expiration time
                user.forgot_password_code = None
                user.forgot_password_code_expires_at = None
                user.save()

                return Response(status=status.HTTP_200_OK)

            return Response(
                {"detail": "This reset code has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return APIException(detail=e)


reset_password_view = ResetPasswordAPIView.as_view()
