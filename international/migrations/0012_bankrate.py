# Generated by Django 3.2.7 on 2021-10-15 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0011_alter_president_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('next_meeting_date', models.DateField()),
                ('central_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='central_bank_rate', to='international.country')),
            ],
        ),
    ]