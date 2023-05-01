from rest_framework.response import Response
from rest_framework import status


def check_is_collector(request):
    error_response = Response(
        {"detail": "You do not have permission to access this resource"},
        status=status.HTTP_403_FORBIDDEN,
    )

    collector = request.user

    if collector.is_verified:
        if collector.is_authenticated and collector.user_type == 3:
            return None
        else:
            return error_response

    return error_response
