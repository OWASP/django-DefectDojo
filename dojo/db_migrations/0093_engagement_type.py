# Generated by Django 2.2.20 on 2021-05-02 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0092_is_mitigated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engagement',
            name='eng_type',
        ),
        migrations.DeleteModel(
            name='Engagement_Type',
        ),
    ]
