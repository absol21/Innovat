# Generated by Django 4.2.1 on 2023-08-08 11:39

import base.services
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('location', models.CharField(blank=True, max_length=60, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=base.services.get_path_upload_avatar, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), base.services.validate_image_size])),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]