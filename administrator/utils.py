from rest_framework.response import Response
from rest_framework import status


def check_is_admin(request):
    error_response = Response(
        {"detail": "You do not have permission to access this resource"},
        status=status.HTTP_403_FORBIDDEN,
    )

    if request.user.is_authenticated and request.user.user_type == 1:
        return None

    return error_response
