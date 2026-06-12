from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    phone_number = models.CharField(
        max_length=20,
        unique=True
    )

    is_owner = models.BooleanField(
        default=False
    )

    is_seeker = models.BooleanField(
        default=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )