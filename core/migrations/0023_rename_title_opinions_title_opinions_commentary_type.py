# Generated by Django 4.0.5 on 2022-08-27 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_opinions_title_alter_opinions_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opinions',
            old_name='Title',
            new_name='title',
        ),
        migrations.AddField(
            model_name='opinions',
            name='commentary_type',
            field=models.CharField(choices=[('Opinion', 'Opinion'), ('Analysis', 'Analysis')], default='Analysis', max_length=10),
        ),
    ]
