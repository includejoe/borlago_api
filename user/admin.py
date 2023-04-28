from django.contrib import admin

from . import models


# Register your models here.
class User(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "gender",
        "user_type",
        "created_at",
    )


admin.site.register(models.User, User)


class Location(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "longitude",
        "latitude",
        "address",
        "created_at",
    )


admin.site.register(models.Location, Location)


class CollectorUnit(admin.ModelAdmin):
    list_display = (
        "id",
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
