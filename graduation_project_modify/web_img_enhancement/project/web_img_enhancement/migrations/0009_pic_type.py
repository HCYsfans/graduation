# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-02-06 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_img_enhancement', '0008_handletypes_trackid'),
    ]

    operations = [
        migrations.AddField(
            model_name='pic',
            name='type',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
