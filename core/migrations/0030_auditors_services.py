# Generated by Django 4.2 on 2023-05-26 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_remove_auditingservices_auditor'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditors',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, to='core.auditingservices'),
        ),
    ]