# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20170927_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(default='a', max_length=1000),
            preserve_default=False,
        ),
    ]