from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0013_publishing_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='availability_status',
            field=models.CharField(
                choices=[
                    ('available', 'Available'),
                    ('rented', 'Rented'),
                    ('sold', 'Sold'),
                    ('hired', 'Hired'),
                    ('unavailable', 'Unavailable')
                ],
                default='available',
                max_length=20
            ),
        ),
    ]
