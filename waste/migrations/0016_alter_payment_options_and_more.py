# Generated by Django 4.1.7 on 2023-05-25 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0015_alter_wastecollectionrequest_waste_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='wastecollectionrequest',
            options={'ordering': ['-created_at']},
        ),
    ]
