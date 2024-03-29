# Generated by Django 4.1.7 on 2023-04-18 22:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_delete_collectorunit'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectorUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='collector_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collectors', to='user.collectorunit'),
        ),
    ]
