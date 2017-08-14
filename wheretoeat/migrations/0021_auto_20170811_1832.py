# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-11 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wheretoeat', '0020_auto_20170809_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='created_en',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='created_tr',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='from_user_en',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='from_user_tr',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='message_en',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='message_tr',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='to_user_en',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='to_user_tr',
        ),
        migrations.RemoveField(
            model_name='display',
            name='displayed_by_en',
        ),
        migrations.RemoveField(
            model_name='display',
            name='displayed_by_tr',
        ),
        migrations.RemoveField(
            model_name='display',
            name='displayed_en',
        ),
        migrations.RemoveField(
            model_name='display',
            name='displayed_tr',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='date_joined_en',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='date_joined_tr',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email_en',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email_tr',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name_en',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name_tr',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='image_en',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='image_tr',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name_en',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name_tr',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_en',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_tr',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username_en',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username_tr',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='checkin_count_en',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='checkin_count_tr',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='name_tr',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='phone_number_en',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='phone_number_tr',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='search_id_en',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='search_id_tr',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='venue_id_en',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='venue_id_tr',
        ),
    ]