import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User, Location, CollectorUnit
from payment.models import Payment


# Create your models here.
class WasteCollectionRequest(models.Model):
    WASTE_TYPE = (
        ("general", "general"),
        ("organic", "organic"),
        ("hazardous", "hazardous"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wcrs")
    pick_up_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="wcrs",
    )
    waste_type = models.CharField(max_length=128, choices=WASTE_TYPE)
    waste_desc = models.TextField(blank=True, null=True)
    waste_quantity = models.IntegerField()
    collector_unit = models.ForeignKey(
        CollectorUnit,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="wcrs",
    )
    collection_datetime = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
    )  # 1 -> Pending, 2 -> In Progress, 3 -> Completed 4, -> Canceled
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wcr",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)