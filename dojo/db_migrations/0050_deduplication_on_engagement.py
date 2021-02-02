# Generated by Django 2.2.14 on 2020-07-26 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0049_create_endpoint_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="engagement",
            name="deduplication_on_engagement",
            field=models.BooleanField(
                default=False,
                help_text="If enabled deduplication will only mark a finding in this engagement as duplicate of another finding if both findings are in this engagement. If disabled, deduplication is on the product level.",
                verbose_name="Deduplication within this engagement only",
            ),
        ),
    ]
