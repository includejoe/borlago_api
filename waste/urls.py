from django.urls import path

from .views import create_wcr_view, make_wcr_payment_view

app_name = "waste"

urlpatterns = [
    path("create/", create_wcr_view, name="create-wcr"),
    path("payment/", make_wcr_payment_view, name="make-wcr-payment"),
]
