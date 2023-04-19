import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


from user.models import User


# Create your models here.
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="payments",
    )
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
                    "transaction_id": "This field can not be null when the payment status is 2 ()"
                }
            )
