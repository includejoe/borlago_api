from django.urls import path, include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("administrator/", include("administrator.urls")),
    path("collector/", include("user.collector_urls")),
    path("user/", include("user.user_urls")),
    path("wcr/", include("waste.urls")),
]
