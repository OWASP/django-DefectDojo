# Generated by Django 2.2.17 on 2021-03-06 16:35

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0083_remove_ipscan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finding_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dojo.Dojo_User')),
                ('findings', models.ManyToManyField(to='dojo.Finding')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]