# Generated by Django 4.2 on 2023-05-30 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_sharesplit'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
    ]
