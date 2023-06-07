from django.urls import path

from .views import (
    create_wcr_view,
    make_wcr_payment_view,
    list_user_wcrs_view,
    wcr_detail_view,
)

app_name = "waste"

urlpatterns = [
    path("create/", create_wcr_view, name="create-wcr"),
    path("user/all/", list_user_wcrs_view, name="user-wcrs"),
    path("detail/<str:wcr_id>/", wcr_detail_view, name="wcr-detail"),
    path("payment/", make_wcr_payment_view, name="make-wcr-payment"),
]
