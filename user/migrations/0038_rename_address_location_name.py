# Generated by Django 4.2.2 on 2023-06-07 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0037_remove_location_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='address',
            new_name='name',
        ),
    ]
