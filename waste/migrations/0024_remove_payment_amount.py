# Generated by Django 4.2.2 on 2023-06-21 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0023_remove_payment_account_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amount',
        ),
    ]
