from django.db import migrations, models


def seed_payment_methods(apps, schema_editor):

    PublishingPaymentMethod = apps.get_model(
        'properties',
        'PublishingPaymentMethod'
    )

    payment_methods = [
        {
            'code': 'mpesa',
            'name': 'M-Pesa',
            'lipa_number': 'ADD_M_PESA_LIPA_NUMBER',
            'instructions': 'Use the listing reference as the account number, then enter the M-Pesa transaction code.',
            'sort_order': 1,
        },
        {
            'code': 'airtel_money',
            'name': 'Airtel Money',
            'lipa_number': 'ADD_AIRTEL_MONEY_LIPA_NUMBER',
            'instructions': 'Use the listing reference as the account number, then enter the Airtel Money transaction code.',
            'sort_order': 2,
        },
        {
            'code': 'halopesa',
            'name': 'HaloPesa',
            'lipa_number': 'ADD_HALOPESA_LIPA_NUMBER',
            'instructions': 'Use the listing reference as the account number, then enter the HaloPesa transaction code.',
            'sort_order': 3,
        },
        {
            'code': 'yas',
            'name': 'Yas',
            'lipa_number': 'ADD_YAS_LIPA_NUMBER',
            'instructions': 'Use the listing reference as the account number, then enter the Yas transaction code.',
            'sort_order': 4,
        },
        {
            'code': 'credit_card',
            'name': 'Credit Card',
            'lipa_number': '',
            'instructions': 'Use the card payment link or contact admin for credit card payment instructions, then enter the payment reference.',
            'sort_order': 5,
        },
    ]

    for payment_method in payment_methods:

        PublishingPaymentMethod.objects.update_or_create(
            code=payment_method['code'],
            defaults=payment_method
        )


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_listing_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishingPaymentMethod',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'code',
                    models.CharField(
                        choices=[
                            ('mpesa', 'M-Pesa'),
                            ('airtel_money', 'Airtel Money'),
                            ('halopesa', 'HaloPesa'),
                            ('yas', 'Yas'),
                            ('credit_card', 'Credit Card')
                        ],
                        max_length=30,
                        unique=True
                    )
                ),
                (
                    'name',
                    models.CharField(
                        max_length=80
                    )
                ),
                (
                    'lipa_number',
                    models.CharField(
                        blank=True,
                        max_length=100
                    )
                ),
                (
                    'instructions',
                    models.TextField(
                        blank=True
                    )
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True
                    )
                ),
                (
                    'sort_order',
                    models.PositiveIntegerField(
                        default=0
                    )
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True
                    )
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True
                    )
                ),
            ],
            options={
                'ordering': ('sort_order', 'name'),
            },
        ),
        migrations.RunPython(
            seed_payment_methods,
            migrations.RunPython.noop
        ),
    ]
