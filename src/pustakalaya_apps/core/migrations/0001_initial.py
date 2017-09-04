# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, verbose_name='Item Category')),
                ('category_description', models.TextField(verbose_name='Item category description')),
            ],
        ),
    ]