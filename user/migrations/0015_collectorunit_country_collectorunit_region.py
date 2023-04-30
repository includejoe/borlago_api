# Generated by Django 4.1.7 on 2023-04-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_remove_user_latitude_remove_user_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectorunit',
            name='country',
            field=models.CharField(default='gh', max_length=24, unique=True),
        ),
        migrations.AddField(
            model_name='collectorunit',
            name='region',
            field=models.CharField(default='ga', max_length=24, unique=True),
        ),
    ]
