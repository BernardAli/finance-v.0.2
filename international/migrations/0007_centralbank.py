# Generated by Django 3.2.7 on 2021-10-13 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0006_president'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentralBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('logo', models.ImageField(default='sector.png', upload_to='presidents')),
                ('url', models.CharField(max_length=255)),
                ('governor', models.CharField(max_length=255)),
                ('dep_governor', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='central_bank', to='international.country')),
            ],
        ),
    ]
