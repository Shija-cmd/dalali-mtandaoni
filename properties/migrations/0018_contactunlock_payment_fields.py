from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0017_contactunlock'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactunlock',
            name='payment_status',
            field=models.CharField(
                choices=[
                    ('unpaid', 'Unpaid'),
                    ('pending', 'Pending Confirmation'),
                    ('paid', 'Paid'),
                    ('rejected', 'Rejected'),
                ],
                default='unpaid',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='contactunlock',
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
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name='contactunlock',
            name='payment_reference',
            field=models.CharField(
                blank=True,
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name='contactunlock',
            name='payment_note',
            field=models.TextField(
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='contactunlock',
            name='payment_rejection_reason',
            field=models.TextField(
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name='contactunlock',
            name='payment_submitted_at',
            field=models.DateTimeField(
                blank=True,
                null=True,
            ),
        ),
    ]
