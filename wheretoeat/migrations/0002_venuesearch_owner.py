# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-01 11:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wheretoeat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuesearch',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
