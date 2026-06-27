from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0014_listing_availability_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listing_rejection_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='payment_rejection_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='verificationrequest',
            name='rejection_reason',
            field=models.TextField(blank=True),
        ),
    ]
