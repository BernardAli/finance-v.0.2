# Generated by Django 3.2.7 on 2021-10-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0021_bourse_about'),
        ('core', '0012_auto_20211021_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyprofile',
            name='index',
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='index',
            field=models.ManyToManyField(blank=True, to='international.Indice'),
        ),
    ]