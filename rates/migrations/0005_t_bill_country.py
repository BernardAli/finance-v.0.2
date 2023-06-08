# Generated by Django 4.2 on 2023-06-07 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0050_alter_continent_continent'),
        ('rates', '0004_mpr_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_bill',
            name='country',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='international.country'),
        ),
    ]
