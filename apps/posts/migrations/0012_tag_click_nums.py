# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-25 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20170420_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='click_nums',
            field=models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u91cf'),
        ),
    ]
