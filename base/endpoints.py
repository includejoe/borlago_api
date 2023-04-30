from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("administrator/", include("administrator.urls")),
    path("collector/", include("collector.urls")),
    path("user/", include("user.urls")),
    path("wcr/", include("waste.urls")),
]
