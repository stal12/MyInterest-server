# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 18:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_category_person'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='second_name',
            new_name='last_name',
        ),
    ]