# Generated by Django 4.2 on 2023-06-04 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0050_alter_continent_continent'),
        ('core', '0043_sharedetail_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EconomicCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('event', models.CharField(max_length=255)),
                ('actual', models.IntegerField()),
                ('forecast', models.IntegerField()),
                ('previous', models.IntegerField()),
                ('file', models.FileField(upload_to='calendar')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='international.country')),
            ],
        ),
    ]