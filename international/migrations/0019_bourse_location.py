# Generated by Django 3.2.7 on 2021-10-18 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0018_auto_20211018_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='bourse',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]