# Generated by Django 3.2.7 on 2021-11-05 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0028_unemployment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Unemployment',
            new_name='UnemploymentRate',
        ),
    ]