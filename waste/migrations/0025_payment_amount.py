# Generated by Django 4.2.2 on 2023-06-21 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0024_remove_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]