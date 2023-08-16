# Generated by Django 4.2.1 on 2023-08-10 14:26

import base.services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=base.services.get_path_upload_book, validators=[base.services.validate_image_size]),
        ),
    ]