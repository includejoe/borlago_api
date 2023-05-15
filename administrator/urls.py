from django.urls import path

from .views import (
    create_collector_unit_view,
    add_collector_to_unit_view,
    get_collectors_view,
    get_collector_units_view,
    collector_detail_view,
    collector_unit_detail_view,
    get_wcrs_view,
    wcr_detail_view,
)

app_name = "administrator"

urlpatterns = [
    path(
        "collector-unit/create/",
        create_collector_unit_view,
        name="create-collector-unit",
    ),
    path("collector-unit/all/", get_collector_units_view, name="get-collector-units"),
    path(
        "collector-unit/add/collector/",
        add_collector_to_unit_view,
        name="add-collector-to-unit",
    ),
    path(
        "collector-unit/detail/<str:unit_id>/",
        collector_unit_detail_view,
        name="collector-unit-detail",
    ),
    path("collector/all/", get_collectors_view, name="get-collectors"),
    path(
        "collector/detail/<str:collector_id>/",
        collector_detail_view,
        name="collector-detail",
    ),
    path("wcr/all/", get_wcrs_view, name="get-wcrs"),
    path(
        "wcr/detail/<str:wcr_id>/",
        wcr_detail_view,
        name="wcr-detail",
    ),
]
