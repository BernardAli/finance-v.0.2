# Generated by Django 3.2.7 on 2021-10-30 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0023_auto_20211030_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='majorexports',
            name='export',
            field=models.ManyToManyField(related_name='export', to='international.Commodity_profile'),
        ),
    ]