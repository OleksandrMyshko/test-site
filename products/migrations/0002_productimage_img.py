# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='img',
            field=models.FileField(default=0, upload_to='products_images/'),
            preserve_default=False,
        ),
    ]
