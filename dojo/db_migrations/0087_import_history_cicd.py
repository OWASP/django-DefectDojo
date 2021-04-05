# Generated by Django 2.2.17 on 2021-04-05 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0086_finding_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='branch_tag',
            field=models.CharField(blank=True, help_text='Tag or branch that was tested, a reimport may update this field.', max_length=150, null=True, verbose_name='Branch/Tag'),
        ),
        migrations.AddField(
            model_name='test',
            name='build_id',
            field=models.CharField(blank=True, help_text='Build ID that was tested, a reimport may update this field.', max_length=150, null=True, verbose_name='Build ID'),
        ),
        migrations.AddField(
            model_name='test',
            name='commit_hash',
            field=models.CharField(blank=True, help_text='Commit hash tested, a reimport may update this field.', max_length=150, null=True, verbose_name='Commit Hash'),
        ),
        migrations.AddField(
            model_name='test_import',
            name='branch_tag',
            field=models.CharField(blank=True, help_text='Tag or branch that was tested, a reimport may update this field.', max_length=150, null=True, verbose_name='Branch/Tag'),
        ),
        migrations.AddField(
            model_name='test_import',
            name='build_id',
            field=models.CharField(blank=True, help_text='Build ID that was tested, a reimport may update this field.', max_length=150, null=True, verbose_name='Build ID'),
        ),
        migrations.AddField(
            model_name='test_import',
            name='commit_hash',
            field=models.CharField(blank=True, help_text='Commit hash tested, a reimport may update this field.', max_length=150, null=True, verbose_name='Commit Hash'),
        ),
    ]
