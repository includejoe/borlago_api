# Generated by Django 4.1.7 on 2023-05-01 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_remove_user_collector_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.URLField(blank=True, null=True),
        ),
    ]
