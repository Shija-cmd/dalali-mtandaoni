from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_alter_listing_latitude_alter_listing_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationrequest',
            name='id_document',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='verification_ids/'
            ),
        ),
    ]
