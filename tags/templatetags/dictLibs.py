# -*- coding: utf-8 -*-
"""
自定义标签, 为页面提供字典值自动加载
"""
from tags.models import DMPDict
from django import template

register = template.Library()

"""
    根据字典类型加载字典的 select 列表
    selected 为当前选中的option
"""
def dicts_tag(dict_type, selected):
    dict_list = DMPDict.objects.filter(isUsed=1, dictType=dict_type)
    return {'dict_list': dict_list, 'selected': selected}
register.inclusion_tag("appstag.html")(dicts_tag)


def dict_phone(dict_type, name, type):
    dict_list = DMPDict.objects.filter(isUsed=1, dictType=dict_type)
    return {'dict_list': dict_list, 'name': name, 'type': type}
register.inclusion_tag("phchbtag.html")(dict_phone)


"""
    根据字典dictId dictType获取字典名称
"""
def dict_name(dict_id, dict_type):
    try:
        dict = DMPDict.objects.get(dictId=dict_id, dictType=dict_type)
        return dict.dictName
    except:
        return ''

register.filter('dict_name', dict_name)


