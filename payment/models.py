import uuid
from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True)
