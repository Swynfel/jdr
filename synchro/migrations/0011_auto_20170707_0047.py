# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 22:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('synchro', '0010_auto_20170707_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='maximum',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='activity',
            name='minimum',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='activity',
            name='slots',
            field=models.ManyToManyField(blank=True, related_name='organising', to='synchro.Slot'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]