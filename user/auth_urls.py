from django.urls import path
from .views import (
    register_user_view,
    login_user_view,
    forgot_password_view,
    reset_password_view,
)


app_name = "authentication"

urlpatterns = [
    path("register/", register_user_view, name="register-user"),
    path("login/", login_user_view, name="login-user"),
    path("forgot-password/", forgot_password_view, name="forgot-password"),
    path("reset-password/", reset_password_view, name="reset-password"),
]
