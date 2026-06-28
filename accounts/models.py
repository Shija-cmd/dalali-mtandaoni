from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    profile_picture_url = models.URLField(
        blank=True,
        null=True
    )

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

    @property
    def profile_picture_display_url(self):

        if self.profile_picture_url:
            return self.profile_picture_url

        if not self.profile_picture:
            return ''

        try:
            return self.profile_picture.url
        except Exception:
            return ''