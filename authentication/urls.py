from django.urls import path
from .views import register_user_view, login_user_view

app_name = "authentication"

urlpatterns = [
    path("register/", register_user_view, name="register_user"),
    path("login/", login_user_view, name="login_user"),
]
