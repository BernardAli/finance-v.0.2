# Generated by Django 4.2 on 2023-06-03 15:31

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('avatar', models.ImageField(default='default.jpg', null=True, upload_to='')),
                ('background_img', models.ImageField(default='home-bg.jpg', upload_to='background_pics')),
                ('bio', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, choices=[('Ghana', 'Ghana'), ('Nigeria', 'Nigeria')], max_length=20, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('user_type', models.CharField(blank=True, choices=[('User', 'User'), ('Trader', 'Trader'), ('Admin', 'Admin')], max_length=20, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=20)),
                ('facebook_url', models.URLField(blank=True, max_length=255, null=True)),
                ('twitter_url', models.URLField(blank=True, max_length=255, null=True)),
                ('instagram_url', models.URLField(blank=True, max_length=255, null=True)),
                ('linkedin_url', models.URLField(blank=True, max_length=255, null=True)),
                ('website_url', models.URLField(blank=True, max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ghana_card', models.FileField(blank=True, null=True, upload_to='')),
                ('passport', models.FileField(blank=True, null=True, upload_to='')),
                ('drivers_license', models.FileField(blank=True, null=True, upload_to='')),
                ('water_bill', models.FileField(blank=True, null=True, upload_to='')),
                ('electricity_bill', models.FileField(blank=True, null=True, upload_to='')),
                ('business_certificate', models.FileField(blank=True, null=True, upload_to='')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success')], default='Pending', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]