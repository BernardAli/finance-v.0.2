# Generated by Django 3.2.7 on 2021-10-13 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0002_country_time_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='dialing_code',
            field=models.CharField(default='+233', max_length=5),
        ),
        migrations.AddField(
            model_name='country',
            name='population',
            field=models.PositiveIntegerField(default=30),
        ),
    ]