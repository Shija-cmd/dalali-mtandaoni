from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0016_listing_featured_package_until'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUnlock',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'amount',
                    models.DecimalField(
                        decimal_places=2,
                        default=500,
                        max_digits=10,
                    ),
                ),
                (
                    'is_paid',
                    models.BooleanField(
                        default=False,
                    ),
                ),
                (
                    'unlocked_at',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'expires_at',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                    ),
                ),
                (
                    'listing',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='contact_unlocks',
                        to='properties.listing',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'unique_together': {
                    ('user', 'listing'),
                },
            },
        ),
    ]
