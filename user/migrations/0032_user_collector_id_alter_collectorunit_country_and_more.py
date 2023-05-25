# Generated by Django 4.1.7 on 2023-05-25 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_remove_location_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='collector_id',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='collectorunit',
            name='country',
            field=models.CharField(default='Ghana', editable=False, max_length=24),
        ),
        migrations.AlterField(
            model_name='collectorunit',
            name='region',
            field=models.CharField(default='Greater Accra', max_length=24),
        ),
    ]
