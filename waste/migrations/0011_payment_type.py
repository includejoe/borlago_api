# Generated by Django 4.1.7 on 2023-04-28 21:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0010_remove_wastecollectionrequest_payment_payment_wcr'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
