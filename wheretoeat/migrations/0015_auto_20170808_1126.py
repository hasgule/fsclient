# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-08 08:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wheretoeat', '0014_auto_20170808_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='display',
            name='displayed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='displayed', to=settings.AUTH_USER_MODEL),
        ),
    ]
