from django.db import migrations, models
import django.db.models.deletion


def copy_location_to_description(apps, schema_editor):

    Listing = apps.get_model(
        'properties',
        'Listing'
    )

    for listing in Listing.objects.all():

        listing.location_description = listing.location
        listing.save(
            update_fields=[
                'location_description'
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0018_contactunlock_payment_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                        unique=True,
                    ),
                ),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                    ),
                ),
                (
                    'region',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='districts',
                        to='properties.region',
                    ),
                ),
            ],
            options={
                'ordering': ('name',),
                'unique_together': {('region', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                    ),
                ),
                (
                    'district',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='wards',
                        to='properties.district',
                    ),
                ),
            ],
            options={
                'ordering': ('name',),
                'unique_together': {('district', 'name')},
            },
        ),
        migrations.CreateModel(
            name='StreetArea',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                    ),
                ),
                (
                    'ward',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='streets',
                        to='properties.ward',
                    ),
                ),
            ],
            options={
                'ordering': ('name',),
                'unique_together': {('ward', 'name')},
            },
        ),
        migrations.AddField(
            model_name='listing',
            name='location_description',
            field=models.CharField(
                blank=True,
                max_length=200,
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='region',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='properties.region',
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='district',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='properties.district',
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='ward',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='properties.ward',
            ),
        ),
        migrations.AddField(
            model_name='listing',
            name='street_area',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='properties.streetarea',
            ),
        ),
        migrations.RunPython(
            copy_location_to_description,
            migrations.RunPython.noop
        ),
    ]
