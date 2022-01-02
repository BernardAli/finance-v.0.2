# Generated by Django 3.2.7 on 2021-10-18 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0014_indice_details'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='indice',
            name='summary',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
