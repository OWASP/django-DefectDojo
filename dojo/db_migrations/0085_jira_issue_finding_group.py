# Generated by Django 2.2.17 on 2021-03-06 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0084_finding_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='jira_issue',
            name='finding_group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dojo.Finding_Group'),
        ),
    ]
