# Generated by Django 4.1.7 on 2023-04-30 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0011_payment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wastecollectionrequest',
            name='waste_quantity',
        ),
        migrations.AddField(
            model_name='wastecollectionrequest',
            name='waste_photo',
            field=models.URLField(default='https://example/image.com'),
            preserve_default=False,
        ),
    ]
