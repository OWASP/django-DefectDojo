# Generated by Django 2.2.9 on 2020-02-14 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0032_system_settings_enable_auditlog"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="finding",
            name="duplicate_list",
        ),
    ]
