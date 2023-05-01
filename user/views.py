from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import User
from waste.models import WasteCollectionRequest
from base.utils.validate_collector import check_is_collector


# Create your views here.
class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def retrieve(self, _, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "This user does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            raise APIException(detail=e)

    def patch(self, request, user_id):
        user = request.user
        data = request.data

        try:
            user_to_update = User.objects.get(id=user_id)

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


class ChangePasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PasswordSerializer


change_password_view = ChangePasswordAPIView.as_view()


class ForgottenPasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PasswordSerializer


forgotten_password_view = ForgottenPasswordAPIView.as_view()


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
