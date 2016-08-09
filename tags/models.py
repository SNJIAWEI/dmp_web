# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class APPInfo(models.Model):
    appName = models.CharField(max_length=256, blank=True)
    appDesc = models.TextField(max_length=68, default='', blank=True)
    appType = models.CharField(max_length=68, blank=True, null=True)
    appBssIntr = models.CharField(max_length=68, blank=True, null=True)
    appSex = models.CharField(max_length=68, blank=True, null=True)
    appStage = models.CharField(max_length=68, blank=True,null=True)
    appFlux = models.FloatField(default='0.0', blank=True, null=True)
    appFluxPer = models.FloatField(default='0.0', blank=True, null=True)
    appUsed = models.IntegerField(default='1', blank=True, null=True)

    def __str__(self):
        return self.appName


@python_2_unicode_compatible
class PhoneInfo(models.Model):
    phoneName = models.CharField(max_length=68, blank=True)
    phoneBrand = models.CharField(max_length=68, blank=True, null=True)
    phonePrice = models.CharField(max_length=68, blank=True, null=True)
    phoneFlux = models.FloatField(default=0.0, blank=True, null=True)
    phoneFluxPer = models.FloatField(default=0.0, blank=True, null=True)
    isUsed = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return self.phoneName + " " + str(self.phoneBrand)


@python_2_unicode_compatible
class DMPDict(models.Model):
    dictId = models.CharField('标识', max_length=68,blank=True)
    dictType = models.CharField('类型', max_length=68, blank=True)
    dictName = models.CharField('名称', max_length=32, blank=True)
    isUsed = models.IntegerField('是否在用', default=0, null=True, blank=True)

    class Meta:
        verbose_name = 'dmp_字典'
        verbose_name_plural = 'dmp_字典'

    def __str__(self):
        return str(self.dictId) + "," + self.dictName + "," + self.dictType+"," + str(self.isUsed)


@python_2_unicode_compatible
class LocationInfo(models.Model):
    location = models.CharField(max_length=68, blank=True)
    locationStage = models.CharField(max_length=68, blank=True)
    locationInterest = models.CharField(max_length=68, blank=True)
    locationFlux = models.FloatField(default=0.0, blank=True, null=True)
    locationFluxPer = models.FloatField(default=0.0, blank=True, null=True)
    isUsed = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return self.location


@python_2_unicode_compatible
class ChannelInterest(models.Model):
    # 渠道Id
    cId = models.CharField(max_length=68, blank=True)
    cName = models.CharField(max_length=128, blank=True)
    # 频道Id
    chnId = models.CharField(max_length=68, blank=True)
    chnName = models.CharField(max_length=128, blank=True)
    chnStage = models.CharField(max_length=32, blank=True)
    chnInterest = models.CharField(max_length=256, blank=True)
    isUsed = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return self.cName + "," + self.chnName