from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0019_location_hierarchy'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='owner_id_document',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='listing_owner_ids/'
            ),
        ),
    ]
