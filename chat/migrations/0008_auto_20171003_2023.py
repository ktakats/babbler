# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_room_group_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='group_id',
            field=models.IntegerField(blank=True),
        ),
    ]
