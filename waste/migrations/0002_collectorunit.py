# Generated by Django 4.1.7 on 2023-04-18 21:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectorUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]