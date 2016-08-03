# coding: utf-8
from django.contrib import admin
from tags.models import DMPDict

# Register your models here.
class DMPDictStateFilter(admin.SimpleListFilter):
    title = u'是否在用'
    parameter_name = 'isUsed'

    def lookups(self, request, model_admin):
        return (
            (0, u'禁用'),
            (1, u'在用'),
        )

    def queryset(self, request, queryset):
        if self.value():
            if int(self.value()) == 0:
                return queryset.filter(isUsed=0)
            if int(self.value()) == 1:
                return queryset.filter(isUsed=1)


class DMPDictAdmin(admin.ModelAdmin):
    search_fields = ('dictName', 'dictType')
    list_filter = (DMPDictStateFilter,)
    ordering = ('dictType', 'dictId',)

    def get_dict_state(self, obj):
        if obj.isUsed == 1:
            return u'<span style="color:green;font-weight:bold">%s</span>' %(u'在用',)
        elif obj.isUsed == 0:
            return u'<span style="color:red;font-weight:bold">%s</span>' % (u"禁用",)
        else:
            return u'<span style="color:orange;font-weight:bold">%s</span>' % (u"状态异常",)
    get_dict_state.short_description = u'是否在用'
    get_dict_state.allow_tags = True
    list_display = ('dictId', 'dictType', 'dictName', 'get_dict_state')

    actions = ['make_onused', 'make_unused']
    # 禁用所选的 dmp_字典
    def make_unused(self, request, queryset):
        rows_updated = queryset.update(isUsed=0)
        self.message_user(request, "%s 条字典被禁用成功。" % str(rows_updated))
    make_unused.short_description = "禁用所选的 dmp_字典"

    # 启用所选的 dmp_字典
    def make_onused(self, request, queryset):
        rows_updated = queryset.update(isUsed=1)
        self.message_user(request, "%s 条字典被启用成功。" % str(rows_updated))
    make_onused.short_description = "启用所选的 dmp_字典"

    # suit 隔行变色
    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'success', 0: 'error', -1: 'error',
        }.get(obj.isUsed)
        if css_class:
            return {'class': css_class, 'data': obj.dictName}

admin.site.register(DMPDict, DMPDictAdmin)