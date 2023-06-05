from django.contrib import admin

from . import models


# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "gender",
        "country",
        "collector_id",
        "user_type",
        "created_at",
    )


admin.site.register(models.User, User)


class Location(admin.ModelAdmin):
    list_display = (
        "id",
        "longitude",
        "latitude",
        "address",
        "created_at",
    )


admin.site.register(models.Location, Location)


class CollectorUnit(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "region",
        "latitude",
        "longitude",
        "available",
        "created_at",
        "updated_at",
    )


admin.site.register(models.CollectorUnit, CollectorUnit)
