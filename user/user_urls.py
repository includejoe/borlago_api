from django.urls import path
from .views import (
    user_detail_view,
    change_password_view,
    forgot_password_view,
    add_location_view,
    list_locations_view,
    delete_location_view,
    add_payment_method_view,
    payment_method_detail_view,
    list_payment_methods_view,
)

app_name = "user"

urlpatterns = [
    path(
        "detail/<str:email>/",
        user_detail_view,
        name="user-detail",
    ),
    path(
        "location/add/",
        add_location_view,
        name="create-location",
    ),
    path(
        "location/all/",
        list_locations_view,
        name="list-locations",
    ),
    path(
        "location/delete/<str:location_id>/",
        delete_location_view,
        name="delete-location",
    ),
    path(
        "payment-method/add/",
        add_payment_method_view,
        name="add-payment-method",
    ),
    path(
        "payment-method/detail/<str:method_id>/",
        payment_method_detail_view,
        name="payment-method-detail",
    ),
    path(
        "payment-method/all/",
        list_payment_methods_view,
        name="list-payment-methods",
    ),
    path(
        "password/change/",
        change_password_view,
        name="change-password",
    ),
    path(
        "password/forgot/",
        forgot_password_view,
        name="forgot-password",
    ),
]
