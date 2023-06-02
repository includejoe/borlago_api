from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView

from . import serializers
from user.models import User


# Create your views here.
class RegistrationAPIView(GenericAPIView):
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


class LoginAPIView(GenericAPIView):
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
