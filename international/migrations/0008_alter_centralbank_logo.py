# Generated by Django 3.2.7 on 2021-10-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0007_centralbank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centralbank',
            name='logo',
            field=models.ImageField(default='sector.png', upload_to='central_banks'),
        ),
    ]