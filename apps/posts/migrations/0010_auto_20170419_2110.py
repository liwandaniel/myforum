# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-19 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20170417_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(related_name='post', to='posts.Tag', verbose_name='\u6807\u7b7e'),
        ),
    ]