from decimal import Decimal

from django.db import migrations


def populate_publishing_fees(apps, schema_editor):
    Listing = apps.get_model('properties', 'Listing')

    for listing in Listing.objects.all():
        listing.publishing_fee = listing.price * Decimal('0.05')
        listing.save(
            update_fields=[
                'publishing_fee',
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0010_listing_payment_fields'),
    ]

    operations = [
        migrations.RunPython(
            populate_publishing_fees,
            migrations.RunPython.noop
        ),
    ]
