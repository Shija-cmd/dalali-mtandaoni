from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture_url',
            field=models.URLField(
                blank=True,
                null=True
            ),
        ),
    ]
