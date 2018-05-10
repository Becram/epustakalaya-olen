# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-10 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import pustakalaya_apps.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0028_auto_20180510_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_total_page',
            field=models.CharField(blank=True, max_length=7, validators=[pustakalaya_apps.core.validators.validate_number], verbose_name='Total Pages'),
        ),
    ]
