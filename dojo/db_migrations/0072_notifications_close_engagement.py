# Generated by Django 2.2.17 on 2021-02-05 19:29

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0071_product_type_enhancement'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='close_engagement',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('slack', 'slack'), ('msteams', 'msteams'), ('mail', 'mail'), ('alert', 'alert')], default='alert', max_length=24),
        ),
    ]
