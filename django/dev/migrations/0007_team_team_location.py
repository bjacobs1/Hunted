# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 21:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dev', '0006_auto_20170909_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='dev.Location'),
        ),
    ]
