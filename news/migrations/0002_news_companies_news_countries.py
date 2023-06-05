# Generated by Django 4.2 on 2023-06-02 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_sharedetail_status'),
        ('international', '0049_population_population'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='companies',
            field=models.ManyToManyField(blank=True, related_name='companies', to='core.companyprofile'),
        ),
        migrations.AddField(
            model_name='news',
            name='countries',
            field=models.ManyToManyField(blank=True, related_name='countries', to='international.country'),
        ),
    ]