# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 03:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wapps', '0019_identity_youtube'),
    ]
    run_before = [
        ('wagtailimages', '0016_deprecate_rendition_filter_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wappsrendition',
            name='filter_spec',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='wappsrendition',
            name='focal_point_key',
            field=models.CharField(blank=True, default='', editable=False, max_length=16),
        ),
        migrations.AlterUniqueTogether(
            name='wappsrendition',
            unique_together=set([('image', 'filter_spec', 'focal_point_key')]),
        ),
    ]
