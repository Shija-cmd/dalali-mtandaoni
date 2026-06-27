from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0015_rejection_reasons'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='featured_package',
            field=models.CharField(
                blank=True,
                choices=[
                    ('featured_7', 'Featured - 7 days'),
                    ('premium_30', 'Premium - 30 days'),
                    ('spotlight_30', 'Homepage Spotlight - 30 days'),
                ],
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='featured_until',
            field=models.DateTimeField(
                blank=True,
                null=True,
            ),
        ),
    ]
