import uuid
import time
import random
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User, Location, CollectorUnit, PaymentMethod


# Create your models here.
class WasteCollectionRequest(models.Model):
    WASTE_TYPE = (
        ("General", "General"),
        ("Organic", "Organic"),
        ("Hazardous", "Hazardous"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.CharField(
        max_length=128, null=False, blank=False, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wcrs")
    pick_up_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="wcrs",
    )
    price = models.DecimalField(
        max_digits=15, decimal_places=2, null=False, blank=False
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

    def generate_public_id(self):
        timestamp = str(int(time.time()))[-8:]  # Get current Unix timestamp
        random_number = str(random.randint(100000, 999999))  # Get random 6 digit number
        counter = str(self.__class__.objects.count() + 1).zfill(
            8
        )  # Get current number of wcrs

        public_id = timestamp + random_number + counter[-2]
        public_id = "WCR-" + str(public_id[8:]).zfill(8)
        return public_id

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.public_id = self.generate_public_id()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wcr = models.ForeignKey(
        WasteCollectionRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="payments",
    )
    method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="used_on_payments",
    )
    account_no = models.CharField(max_length=255, null=False, blank=False)
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

    class Meta:
        ordering = ["-created_at"]
