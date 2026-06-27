from django.db import migrations, models


def mark_existing_approved_listings_paid(apps, schema_editor):
    Listing = apps.get_model('properties', 'Listing')
    Listing.objects.filter(
        is_approved=True
    ).update(
        payment_status='paid'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_verificationrequest_id_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='publishing_fee',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='payment_status',
            field=models.CharField(
                choices=[
                    ('unpaid', 'Unpaid'),
                    ('pending', 'Pending Confirmation'),
                    ('paid', 'Paid'),
                    ('rejected', 'Rejected'),
                ],
                default='unpaid',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='payment_reference',
            field=models.CharField(
                blank=True,
                max_length=100
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='payment_note',
            field=models.TextField(
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='payment_submitted_at',
            field=models.DateTimeField(
                blank=True,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='paid_at',
            field=models.DateTimeField(
                blank=True,
                null=True
            ),
        ),
        migrations.RunPython(
            mark_existing_approved_listings_paid,
            migrations.RunPython.noop
        ),
    ]
