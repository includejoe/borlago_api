from django.urls import path
from .views import user_detail_view, change_password_view, forgotten_password_view

app_name = "user"

urlpatterns = [
    path("detail/<str:email>/", user_detail_view, name="user-detail"),
    path("password/change/", change_password_view, name="change-password"),
    path("password/forgot/", forgotten_password_view, name="forgot-password"),
]
