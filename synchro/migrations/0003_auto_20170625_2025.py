# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synchro', '0002_auto_20170625_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]