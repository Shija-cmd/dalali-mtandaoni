from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0020_listing_owner_id_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingimage',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='listing_images/'
            ),
        ),
        migrations.AddField(
            model_name='listingimage',
            name='image_url',
            field=models.URLField(
                blank=True,
                null=True
            ),
        ),
    ]
