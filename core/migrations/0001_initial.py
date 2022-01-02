# Generated by Django 3.2.7 on 2021-09-16 22:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('international', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_id', models.CharField(max_length=10)),
                ('logo', models.ImageField(default='sector.png', upload_to='company')),
                ('isin', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('postal_address', models.CharField(blank=True, max_length=255, null=True)),
                ('registered_office', models.CharField(blank=True, max_length=255, null=True)),
                ('incorporated_date', models.DateField(blank=True, null=True)),
                ('telephone', models.CharField(blank=True, max_length=20, null=True)),
                ('toll_free', models.CharField(blank=True, max_length=20, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('core_activities', models.TextField()),
                ('summary', models.TextField(blank=True, max_length=2500, null=True)),
                ('country', models.ForeignKey(default='Ghana', on_delete=django.db.models.deletion.CASCADE, to='international.country')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(choices=[('Q1', '1st Quarter'), ('H1', '1st Half'), ('9M', '9 Months'), ('FY', 'Full Year')], max_length=50)),
                ('slug', models.SlugField(default='fy', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=255)),
                ('icon', models.ImageField(default='sector.png', upload_to='sector')),
                ('slug', models.SlugField(default='GSE', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarketReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('file', models.FileField(upload_to='reports')),
                ('session_number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=255)),
                ('icon', models.ImageField(default='sector.png', upload_to='sector')),
                ('slug', models.SlugField(default='financial', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Tag')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='SharePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('volume', models.PositiveBigIntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ShareDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_shares', models.PositiveBigIntegerField()),
                ('stated_capital', models.PositiveBigIntegerField(blank=True, null=True)),
                ('listed_date', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Secretary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('logo', models.ImageField(default='sector.png', upload_to='auditors')),
                ('slug', models.SlugField(default='None', unique=True)),
                ('company', models.ManyToManyField(blank=True, related_name='secretary', to='core.CompanyProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DateField()),
                ('file', models.FileField(upload_to='reports')),
                ('audited', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.companyprofile')),
                ('period', models.ManyToManyField(to='core.FinancialPeriod')),
            ],
        ),
        migrations.CreateModel(
            name='PressRelease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='reports')),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.companyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='KeyPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('picture', models.ImageField(default='sector.png', upload_to='key_pople')),
                ('birth_date', models.DateField()),
                ('highest_education', models.CharField(max_length=250)),
                ('position', models.CharField(choices=[('CEO', 'CEO'), ('Chairman', 'Chairman')], max_length=50)),
                ('company', models.ManyToManyField(blank=True, related_name='key_people', to='core.CompanyProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Indices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='international.indice')),
            ],
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='industry',
            field=models.ManyToManyField(blank=True, related_name='tags', to='core.Tag'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='market',
            field=models.ManyToManyField(default='GSE', related_name='tags', to='core.Market'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='sector',
            field=models.ManyToManyField(blank=True, related_name='tags', to='core.Sector'),
        ),
        migrations.CreateModel(
            name='Auditors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('logo', models.ImageField(default='sector.png', upload_to='auditors')),
                ('company', models.ManyToManyField(blank=True, related_name='auditors', to='core.CompanyProfile')),
            ],
        ),
    ]