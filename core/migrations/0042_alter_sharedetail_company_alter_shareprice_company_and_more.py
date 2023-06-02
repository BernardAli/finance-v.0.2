# Generated by Django 4.2 on 2023-06-01 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_alter_companyprofile_share_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedetail',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_details', to='core.companyprofile'),
        ),
        migrations.AlterField(
            model_name='shareprice',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_price', to='core.companyprofile'),
        ),
        migrations.AlterField(
            model_name='sharesplit',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_splits', to='core.companyprofile'),
        ),
    ]
