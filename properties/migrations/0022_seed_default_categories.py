from django.db import migrations

from properties.category_seed import seed_default_categories


def seed_categories(apps, schema_editor):

    category_model = apps.get_model(
        'properties',
        'Category'
    )

    seed_default_categories(
        category_model
    )


class Migration(migrations.Migration):

    dependencies = [
        (
            'properties',
            '0021_listingimage_image_url_and_nullable_image'
        ),
    ]

    operations = [
        migrations.RunPython(
            seed_categories,
            migrations.RunPython.noop
        ),
    ]
