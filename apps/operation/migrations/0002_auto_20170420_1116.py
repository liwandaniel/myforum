# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-20 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_type',
            field=models.IntegerField(choices=[(1, '\u6587\u7ae0'), (2, '\u6807\u7b7e')], default=1, verbose_name='\u6536\u85cf\u7c7b\u578b'),
        ),
    ]
