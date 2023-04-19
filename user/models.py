import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        email,
        gender,
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
        user.phone = phone
        user.user_type = user_type
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.save()

        return user

    def create_superuser(self, first_name, last_name, email, gender, phone, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
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
class CollectorUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (("male", "male"), ("female", "female"), ("other", "other"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=128, default="+233")
    gender = models.CharField(max_length=56, default="Other", choices=GENDER_CHOICES)
    is_staff = models.BooleanField(default=False)
    collector_unit = models.ForeignKey(
        CollectorUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collectors",
    )
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "gender"]

    objects = UserManager()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def clean(self):
        if self.user_type != 3 and self.collector_unit is not None:
            raise ValidationError(
                {
                    "collector_unit": "A user of type not equal to 3 can not belong to a collection unit"
                }
            )

    class Meta:
        ordering = ["-created_at"]


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")
    picture = models.URLField(blank=False, null=False)
    name = models.CharField(max_length=1024, null=False, blank=False)
    address = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
