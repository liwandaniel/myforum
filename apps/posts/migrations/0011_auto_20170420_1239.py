# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-20 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20170419_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='\u6536\u85cf\u4eba\u6570'),
        ),
        migrations.AddField(
            model_name='tag',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='\u6536\u85cf\u4eba\u6570'),
        ),
    ]