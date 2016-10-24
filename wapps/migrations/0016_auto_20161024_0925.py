# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wapps', '0015_identitysettings_amp_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identitysettings',
            name='amp_logo',
            field=models.ForeignKey(blank=True, help_text='An mobile optimized logo that must be 600x60', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wapps.WappsImage', verbose_name='Mobile Logo'),
        ),
    ]
