def check_is_admin(request):
    if request.user.is_authenticated and request.user.user_type == 1:
        return True

    return False
