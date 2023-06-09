import uuid
import time
import random
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from base.utils.country_codes import country_codes


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        email,
        gender,
        country,
        phone,
        user_type=2,
        password=None,
        is_superuser=False,
        is_staff=False,
    ):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.country = country
        user.phone = phone
        user.user_type = user_type
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.save()

        return user

    def create_superuser(
        self, first_name, last_name, email, gender, country, phone, password
    ):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            country=country,
            phone=phone,
            password=password,
            user_type=1,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    COUNTRY_CHOICES = ((country, country) for country in country_codes.keys())

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=128, default="233")
    momo_number = models.CharField(max_length=128, null=True, blank=True)
    gender = models.CharField(max_length=12, default="Other")
    country = models.CharField(max_length=64, default="Ghana", choices=COUNTRY_CHOICES)
    is_staff = models.BooleanField(default=False)
    user_type = models.PositiveSmallIntegerField(
        default=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(3),
        ],
    )  # 1 -> Admin, 2 -> Normal User, 3 -> Collector
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # COLLECTOR SPECIFIC FIELDS
    is_verified = models.BooleanField(default=None, null=True, blank=True)
    is_suspended = models.BooleanField(default=None, null=True, blank=True)
    profile_photo = models.URLField(null=True, blank=True)
    collector_id = models.CharField(max_length=128, null=True, blank=True, unique=True)
    collector_unit = models.ForeignKey(
        "CollectorUnit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collectors",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "gender"]

    objects = UserManager()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def clean(self):
        if self.user_type != 3:
            if self.collector_unit is not None:
                raise ValidationError(
                    {
                        "collector_unit": "A user of type not equal to 3(collector) can not belong to a collection unit"
                    }
                )
            if self.is_verified is not None:
                raise ValidationError(
                    {
                        "is_verified": "A user of type not equal to 3(collector) must have this field set to null"
                    }
                )
            if self.is_suspended is not None:
                raise ValidationError(
                    {
                        "is_suspended": "A user of type not equal to 3(collector) must have this field set to null"
                    }
                )
            if self.profile_photo is not None:
                raise ValidationError(
                    {
                        "profile_photo": "A user of type not equal to 3(collector) must have this field set to null"
                    }
                )

    def generate_collector_id(self):
        timestamp = str(int(time.time()))[-6:]  # Get current Unix timestamp
        random_number = str(random.randint(100000, 999999))  # Get random 6 digit number
        counter = str(self.__class__.objects.count() + 1).zfill(
            6
        )  # Get current number of users

        collector_id = timestamp + random_number + counter[-2:]
        return collector_id[:6]

    def save(self, *args, **kwargs):
        collector_id = self.collector_id

        if self._state.adding:
            if self.user_type == 3:
                if collector_id is None:
                    self.collector_id = self.generate_collector_id()
                else:
                    raise ValidationError(
                        {"collector_id": "A collector must have a collector_id"}
                    )

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class CollectorUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        null=False,
        blank=False,
    )
    country = models.CharField(max_length=24, default="Ghana", editable=False)
    region = models.CharField(max_length=24, default="Greater Accra")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collector_units_created",
    )
    updated_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collector_units_updated",
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    # Generate unique name
    def save(self, *args, **kwargs):
        country = self.country

        if country in country_codes:
            country_code = country_codes[country]
        else:
            raise ValidationError({"detail": "This country is not supported"})

        if self._state.adding:
            last_instance = (
                CollectorUnit.objects.filter(country=country).order_by("-id").first()
            )
            if last_instance:
                last_name = last_instance.name
                if int(last_name[3:]) >= 9999:
                    last_alpha = chr(ord(last_name[2]) + 1)
                    new_name = f"{country_code}{last_alpha}0001"
                else:
                    new_name = f"{country_code}{last_name[2:]}"
                    new_name = f"{new_name[:3]}{int(new_name[3:])+1:04d}"
            else:
                new_name = f"{country_code}A0001"

            while CollectorUnit.objects.filter(name=new_name).exists():
                # Generate a new unique name if the current name already exists in the database
                if int(new_name[3:]) >= 9999:
                    last_alpha = chr(ord(new_name[2]) + 1)
                    new_name = f"{country_code}{last_alpha}0001"
                else:
                    new_name = f"{country_code}{new_name[2:]}"
                    new_name = f"{new_name[:3]}{int(new_name[3:])+1:04d}"

            self.name = new_name

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=1024, null=False, blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class PaymentMethod(models.Model):
    PAYMENT_METHODS = (("Mobile Money", "Mobile Money"), ("Bank Card", "Bank Card"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        max_length=24, choices=PAYMENT_METHODS, null=False, blank=False
    )
    name = models.CharField(max_length=128, null=False, blank=False)
    account_number = models.CharField(max_length=128, null=False, blank=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payment_methods",
    )

    # Bank Card Details
    expiry_date = models.CharField(max_length=5, null=True, blank=True)
    name_on_card = models.CharField(max_length=128, null=True, blank=True)
    security_code = models.CharField(max_length=3, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        if self.type == "Bank Card":
            if not self.expiry_date:
                raise ValidationError({"expiry_date": "This field is required"})
            if not self.name_on_card:
                raise ValidationError({"name_on_card": "This field is required"})
            if not self.security_code:
                raise ValidationError({"security_code": "This field is required"})
            if not self.zip_code:
                raise ValidationError({"zip_code": "This field is required"})
        return super().clean()

    class Meta:
        ordering = ["-created_at"]
