# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_result'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['p_parameter']},
        ),
        migrations.AddField(
            model_name='result',
            name='time',
            field=models.FloatField(null=True),
        ),
    ]
