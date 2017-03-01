# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0007_auto_20170228_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choicequestion',
            name='visible',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='visible',
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='vendors',
            field=models.ManyToManyField(blank=True, to='rsvp.Vendor'),
        ),
        migrations.AddField(
            model_name='textquestion',
            name='vendors',
            field=models.ManyToManyField(blank=True, to='rsvp.Vendor'),
        ),
    ]
