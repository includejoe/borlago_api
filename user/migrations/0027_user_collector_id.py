# Generated by Django 4.1.7 on 2023-04-30 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_collectorunit_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='collector_id',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True, unique=True),
        ),
    ]
