# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synchro', '0004_auto_20170703_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='tag',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='link',
            field=models.CharField(default='aventure', max_length=16, unique=True),
            preserve_default=False,
        ),
    ]