# Generated by Django 4.1.7 on 2023-05-01 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0012_remove_wastecollectionrequest_waste_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wastecollectionrequest',
            name='is_collected',
            field=models.BooleanField(default=False),
        ),
    ]
