# Generated by Django 2.2.15 on 2020-08-30 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0050_deduplication_on_engagement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="regulation",
            name="category",
            field=models.CharField(
                choices=[
                    ("privacy", "Privacy"),
                    ("finance", "Finance"),
                    ("education", "Education"),
                    ("medical", "Medical"),
                    ("corporate", "Corporate"),
                    ("other", "Other"),
                ],
                help_text="The subject of the regulation.",
                max_length=9,
            ),
        ),
        migrations.AlterField(
            model_name="regulation",
            name="name",
            field=models.CharField(
                help_text="The name of the regulation.", max_length=128, unique=True
            ),
        ),
    ]
