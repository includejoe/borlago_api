# Generated by Django 4.1.7 on 2023-04-18 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickUpLocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('picture', models.URLField()),
                ('name', models.CharField(max_length=1024)),
                ('address', models.CharField(max_length=1024)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pick_up_locations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
