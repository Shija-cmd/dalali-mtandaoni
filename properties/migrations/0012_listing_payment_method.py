from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0011_populate_listing_publishing_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='payment_method',
            field=models.CharField(
                blank=True,
                choices=[
                    ('mpesa', 'M-Pesa'),
                    ('airtel_money', 'Airtel Money'),
                    ('halopesa', 'HaloPesa'),
                    ('yas', 'Yas'),
                    ('credit_card', 'Credit Card'),
                ],
                max_length=30
            ),
        ),
    ]
