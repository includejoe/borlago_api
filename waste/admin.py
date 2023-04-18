from django.contrib import admin

from . import models


# Register your models here.
class WasteCollectionRequest(admin.ModelAdmin):
    list_display = (
        "id",
        "waste_type",
        "waste_desc",
        "waste_quantity",
        "collection_datetime",
        "status",
    )


admin.site.register(models.WasteCollectionRequest, WasteCollectionRequest)
