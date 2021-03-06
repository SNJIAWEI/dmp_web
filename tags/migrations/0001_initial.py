# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-26 03:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APPInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appName', models.CharField(blank=True, max_length=256)),
                ('appDesc', models.TextField(blank=True, default='')),
                ('appType', models.CharField(blank=True, null=True, max_length=68)),
                ('appBssIntr', models.CharField(blank=True,  null=True, max_length=68)),
                ('appSex', models.CharField(blank=True,  null=True, max_length=68)),
                ('appStage', models.CharField(blank=True, null=True, max_length=68)),
                ('appFlux', models.FloatField(blank=True, default='0.0', null=True)),
                ('appFluxPer', models.FloatField(blank=True, default='0.0', null=True)),
                ('appUsed', models.IntegerField(blank=True, default='1', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DMPDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dictId', models.CharField(blank=True, max_length=68)),
                ('dictType', models.CharField(blank=True, max_length=68)),
                ('dictName', models.CharField(blank=True, max_length=32)),
                ('isUsed', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneName', models.CharField(blank=True, max_length=68)),
                ('phoneBrand', models.CharField(blank=True, null=True, max_length=68)),
                ('phonePrice', models.IntegerField(blank=True, default=0, null=True)),
                ('phoneFlux', models.FloatField(blank=True, default=0.0, null=True)),
                ('phoneFluxPer', models.FloatField(blank=True, default=0.0, null=True)),
                ('isUsed', models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
    ]
