# Generated by Django 3.2.7 on 2021-11-05 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0027_auto_20211030_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unemployment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='2020-12-31')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unemployment', to='international.country')),
            ],
        ),
    ]
