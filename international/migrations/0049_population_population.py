# Generated by Django 4.2 on 2023-05-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0048_population'),
    ]

    operations = [
        migrations.AddField(
            model_name='population',
            name='population',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
