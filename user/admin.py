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
    )


admin.site.register(models.User, User)


class PickUpLocation(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "picture",
        "address",
    )


admin.site.register(models.PickUpLocation, PickUpLocation)
