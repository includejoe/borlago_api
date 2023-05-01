import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User, Location, CollectorUnit


# Create your models here.
class WasteCollectionRequest(models.Model):
    WASTE_TYPE = (
        ("general", "general"),
        ("organic", "organic"),
        ("hazardous", "hazardous"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wcrs")
    pick_up_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="wcrs",
    )
    waste_type = models.CharField(max_length=128, choices=WASTE_TYPE)
    waste_desc = models.TextField(blank=True, null=True)
    waste_photo = models.URLField(null=False, blank=False)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wcr = models.ForeignKey(
        WasteCollectionRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment",
    )
    payer = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="payments",
    )
    type = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(2),
        ],
    )  # 1 -> MoMo, 2 -> Cash
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3),
        ],
    )  # 1 -> Pending, 2 -> Paid, 3 -> Canceled
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.status == 2 and self.transaction_id is None:
            raise ValidationError(
                {
                    "transaction_id": "This field can not be null when the payment status is 2"
                }
            )
