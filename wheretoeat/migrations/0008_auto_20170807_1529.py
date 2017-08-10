# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-07 12:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wheretoeat', '0007_auto_20170807_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.FileField(blank=True, default=None, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='venue',
            name='venue_id',
            field=models.CharField(default='something', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
