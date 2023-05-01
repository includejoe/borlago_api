from rest_framework.response import Response
from rest_framework import status


def check_is_admin(request):
    error_response = Response(
        {"detail": "You do not have permission to access this resource"},
        status=status.HTTP_403_FORBIDDEN,
    )

    admin = request.user

    if admin.is_authenticated and admin.user_type == 1:
        return None

    return error_response
