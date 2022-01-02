# Generated by Django 3.2.5 on 2021-09-11 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pair', models.CharField(choices=[('USDGHS', 'USDGHS'), ('GBPGHS', 'GBPGHS'), ('CHFGHS', 'CHFGHS'), ('AUDGHS', 'AUDGHS'), ('CADGHS', 'CADGHS'), ('DKKGHS', 'DKKGHS'), ('JPYGHS', 'JPYGHS'), ('NZDGHS', 'NZDGHS'), ('NOKGHS', 'NOKGHS'), ('SEKGHS', 'SEKGHS'), ('ZARGHS', 'ZARGHS'), ('EURGHS', 'EURGHS'), ('CNYGHS', 'CNYGHS'), ('GHSXOF', 'GHSXOF'), ('GHSGMD', 'GHSGMD'), ('GHSMRO', 'GHSMRO'), ('GHSNGN', 'GHSNGN'), ('GHSSLL', 'GHSSLL'), ('WAUGHS', 'WAUGHS')], max_length=50)),
                ('currency', models.CharField(max_length=50)),
                ('slug', models.SlugField(default='usdghs', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inflation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='MPR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_no', models.PositiveIntegerField(default=1)),
                ('dates', models.CharField(max_length=120)),
                ('effective_date', models.DateField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('security', models.CharField(choices=[('91 DAY BILL', '91 DAY BILL'), ('182 DAY BILL', '182 DAY BILL'), ('364 DAY BILL', '364 DAY BILL'), ('1 YR FXR BOND', '1 YR FXR BOND'), ('2 YR FXR BOND', '2 YR FXR BOND'), ('3 YR FXR BOND', '3 YR FXR BOND'), ('5 YR FXR BOND', '5 YR FXR BOND'), ('6 YR FXR BOND', '6 YR FXR BOND'), ('7 YR FXR BOND', '7 YR FXR BOND'), ('10 YR FXR BOND', '10 YR FXR BOND'), ('15 YR FXR BOND', '15 YR FXR BOND'), ('20 YR FXR BOND', '20 YR FXR BOND')], max_length=50)),
                ('slug', models.SlugField(default='91_DAY_BILL', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='T_BILL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField()),
                ('tender', models.PositiveIntegerField()),
                ('discount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('interest', models.DecimalField(decimal_places=2, max_digits=6)),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rates.security')),
            ],
        ),
        migrations.CreateModel(
            name='InterbankFX',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('buying', models.DecimalField(decimal_places=4, max_digits=8)),
                ('selling', models.DecimalField(decimal_places=4, max_digits=8)),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rates.currencypair')),
            ],
        ),
    ]
