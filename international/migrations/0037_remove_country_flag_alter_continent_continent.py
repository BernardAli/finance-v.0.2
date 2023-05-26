# Generated by Django 4.2 on 2023-05-09 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0036_remove_centralbank_dep_governor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='flag',
        ),
        migrations.AlterField(
            model_name='continent',
            name='continent',
            field=models.CharField(choices=[('Africa', 'Africa'), ('Europe', 'Europe'), ('Middle East', 'Middle East'), ('Asia', 'Asia'), ('Americas', 'Americas'), ('Oceania', 'Oceania')], max_length=50),
        ),
    ]