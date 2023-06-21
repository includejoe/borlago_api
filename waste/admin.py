from django.contrib import admin

from . import models


# Register your models here.
class WasteCollectionRequest(admin.ModelAdmin):
    list_display = (
        "public_id",
        "waste_type",
        "waste_desc",
        "price",
        "collection_datetime",
        "status",
    )


admin.site.register(models.WasteCollectionRequest, WasteCollectionRequest)


class Payment(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "amount",
        "status",
        "created_at",
    )


admin.site.register(models.Payment, Payment)
