# Generated by Django 4.1.7 on 2023-04-28 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_user_momo_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectorunit',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='collectorunit',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='233', max_length=128),
        ),
    ]
