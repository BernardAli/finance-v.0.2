# Generated by Django 4.2 on 2023-05-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auditors_country_auditors_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditors',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]