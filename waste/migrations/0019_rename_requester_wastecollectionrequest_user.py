# Generated by Django 4.2.2 on 2023-06-07 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0018_rename_wcr_id_wastecollectionrequest_public_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wastecollectionrequest',
            old_name='requester',
            new_name='user',
        ),
    ]