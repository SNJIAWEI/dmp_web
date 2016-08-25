# coding: utf-8
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from tags.models import APPInfo, DMPDict, PhoneInfo, LocationInfo, ChannelInterest

# Create your views here.
one_page_num = 15

""" APP查询 """


def appsinfo_main(request):
    page = 1
    page_multi = 1
    searchAppType = ''
    searchAppName = ''
    try:
        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            page_multi = int(request.GET.get('pageMulti', '1'))
            searchAppType = request.GET.get('q', '')
            searchAppName = request.GET.get('appn', '')
            if page < 1:
                page = 1
        if request.method == 'POST':
            searchAppType = str(request.POST['q'])
            searchAppName = request.POST['appn']
    except:
        page = 1
        page_multi = 1
        searchAppType = ''

    apps_list = APPInfo.objects.filter(appUsed=1).order_by("-appFluxPer")
    if len(searchAppType) > 0:
        apps_list = apps_list.filter(appType__in=searchAppType.split(","))
    if len(searchAppName) > 0:
        apps_list = apps_list.filter(appName__contains=searchAppName)

    paginator = Paginator(apps_list, 15)
    try:
        apps_page = paginator.page(page)
    except PageNotAnInteger:
        apps_page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        apps_page = paginator.page(paginator.num_pages)

    has_next = True
    # 总页数大于需要显示的页数
    if one_page_num * page_multi <= paginator.num_pages:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, page_multi * one_page_num + 1)
    else:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, paginator.num_pages + 1)
        has_next = False
    return render(request, 'appsinfo.html', {'apps': apps_page, 'page_curt_range': page_curt_range,
                                             'search_value': searchAppType, 'search_appn': searchAppName,
                                             'pageMulti': page_multi, 'one_page_num': one_page_num,
                                             'has_next': has_next})


""" APP编辑 """


def app_edit(request):
    try:
        page = request.GET.get("p", 1)
        pagemulit = request.GET.get("pm", 1)
        search_value = request.GET.get('q', 1)
        search_appn = request.GET.get('appn', '')
        if request.GET.get("id", None):
            app_obj = APPInfo.objects.filter(appUsed=1).get(id=request.GET.get("id", None))
        interest_type_list = DMPDict.objects.filter(isUsed=1, dictType='兴趣分类').order_by("dictId")
    except:
        app_obj = ''
        page = 1
        pagemulit = 1
        search_value = ''
        search_appn = ''
    return render(request, "appsedit.html", {'app': app_obj, 'interest_type_list': interest_type_list,
                                             'page': page, 'pageMulti': pagemulit, 'search_value': search_value,
                                             'search_appn': search_appn})


""" APP更新 """


def app_update(request):
    if request.method == 'POST':
        try:
            search_value = request.POST['q']
            search_appn = request.POST['appn']
            page = int(request.POST['page'])
            pageMulti = int(request.POST['pageMulti'])
            appInfo_obj = APPInfo.objects.get(id=request.POST['appId'])
            appInfo_obj.appDesc = request.POST['appDesc']
            appInfo_obj.appType = request.POST['appType']
            appInfo_obj.appBssIntr = request.POST['appBssIntr']
            appInfo_obj.appSex = request.POST['appSex']
            appInfo_obj.appStage = request.POST['appStage']

            appInfo_obj.save()
            result = 'success'
        except Exception, ex:
            print Exception, ":", ex
            page = 1
            pageMulti = 1
            result = 'error'
    else:
        result = 'error'
    messages.success(request, result)
    return HttpResponseRedirect("/dmp/appsinfo/?page=" + str(page) + "&&pageMulti=" + str(pageMulti) + "&&q=" + str(
        search_value) + "&&appn=" + unicode(search_appn))


""" 手机标注 - 列表页 """


def phoneinfo_main(request):
    try:
        page = int(request.GET.get('page', '1'))
        page_multi = int(request.GET.get('pageMulti', '1'))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
        page_multi = 1

    telphone_list = PhoneInfo.objects.filter(isUsed=1).order_by("-phoneFluxPer")
    paginator = Paginator(telphone_list, 15)
    try:
        telphone_page = paginator.page(page)
    except PageNotAnInteger:
        telphone_page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        telphone_page = paginator.page(paginator.num_pages)

    has_next = True
    # 总页数大于需要显示的页数
    if one_page_num * page_multi <= paginator.num_pages:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, page_multi * one_page_num + 1)
    else:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, paginator.num_pages + 1)
        has_next = False

    return render(request, 'phoneinfo.html', {'phones': telphone_page, 'page_curt_range': page_curt_range,
                                              'pageMulti': page_multi, 'one_page_num': one_page_num,
                                              'has_next': has_next})


""" 手机编辑 """


def phone_edit(request):
    try:
        page = request.GET.get("p", 1)
        pagemulit = request.GET.get("pm", 1)
        if request.GET.get("id", None):
            phone_obj = PhoneInfo.objects.filter(isUsed=1).get(id=request.GET.get("id", None))
    except:
        phone_obj = ''
        page = 1
        pagemulit = 1
        pass
    return render(request, "phonedit.html", {'telObj': phone_obj, 'page': page, 'pageMulti': pagemulit})


""" 手机编辑 - 保存 """


def phone_update(request):
    if request.method == 'POST':
        try:
            page = int(request.POST['page'])
            pageMulti = int(request.POST['pageMulti'])
            tel_obj = PhoneInfo.objects.get(id=request.POST['telId'])
            tel_obj.phoneBrand = request.POST['phoneBrand']
            tel_obj.phonePrice = request.POST['phonePrice']

            tel_obj.save()
            result = 'success'
        except Exception, ex:
            print Exception, ":", ex
            page = 1
            pageMulti = 1
            result = 'error'
    else:
        result = 'error'
    messages.success(request, result)
    return HttpResponseRedirect("/dmp/phoneinfo/?page=" + str(page) + "&&pageMulti=" + str(pageMulti))


""" 人群构建 """


def struct_people_main(request):
    app_type_list = DMPDict.objects.filter(isUsed=1, dictType='APP类别').order_by("dictId")
    interest_type_list = DMPDict.objects.filter(isUsed=1, dictType='兴趣分类').order_by("dictId")
    often_place_list = DMPDict.objects.filter(isUsed=1, dictType='常去地点').order_by("dictId")
    prov_city_list = DMPDict.objects.filter(isUsed=1, dictType='省市').order_by("dictId")

    tree_xq_dict = {}
    tree_xq_node_dict = {}
    for itl in interest_type_list:
        if len(itl.dictId) == 5:
            tree_xq_dict[itl.dictId] = '{id: "%s", pId: 0, name: "%s", open: false, children:[temp_children]},' % (
                itl.dictId, itl.dictName)
        elif len(itl.dictId) == 9:
            current_key = itl.dictId[0:5]
            if tree_xq_node_dict.has_key(current_key):
                current_cnode = tree_xq_node_dict[current_key]
                tree_xq_node_dict[current_key] = current_cnode + '{id: "%s", name: "%s"},' % (itl.dictId, itl.dictName)
            else:
                tree_xq_node_dict[current_key] = '{id: "%s", name: "%s"},' % (itl.dictId, itl.dictName)
        else:
            pass

    for k, v in tree_xq_dict.items():
        if tree_xq_node_dict.has_key(k):
            tree_xq_dict[k] = v.replace("temp_children", tree_xq_node_dict.get(k))
        else:
            tree_xq_dict[k] = v.replace("children:[temp_children]", "")

    return render(request, "structpeople.html", {"app_type_list": app_type_list,
                                                 "interest_type_dict": tree_xq_dict,
                                                 "often_place_list": often_place_list,
                                                 "prov_city_list": prov_city_list})


""" 标签管理 - 位置信息 """


def locations_main(request):
    locations_dict = DMPDict.objects.filter(dictType='常去地点')
    locations_list = LocationInfo.objects.all()
    len_locations_list = locations_list.count()

    if len_locations_list == 0:
        locations_batch = []
        for ld in locations_dict.filter(isUsed=1):
            locations_batch.append(LocationInfo(location=ld.dictId))
        LocationInfo.objects.bulk_create(locations_batch)

        locations_list = locations_list.order_by("-locationFluxPer")
    else:
        location_unused_dict = locations_dict.filter(isUsed=0)
        if location_unused_dict.count() > 0:
            for lud in location_unused_dict:
                try:
                    LocationInfo.objects.get(lud.dictId).delete()
                except:
                    pass
        else:
            location_used_dict = locations_dict.filter(isUsed=1)
            if location_used_dict.count() > len_locations_list:
                locations_batch = []
                for ld in location_used_dict:
                    if locations_list.filter(location=ld.dictId).count() == 0:
                        locations_batch.append(LocationInfo(location=ld.dictId))
                    else:
                        pass
                LocationInfo.objects.bulk_create(locations_batch)
            else:
                pass
            locations_list = locations_list.order_by("-locationFluxPer")
    return render(request, "locations.html", {"locations": locations_list})


"""
    标签管理 - 位置信息 [编辑]
"""


def locations_edit(request):
    location_obj = ''
    try:
        if request.method == 'GET':
            locationId = request.GET.get('id', None)
            location_obj = LocationInfo.objects.get(id=locationId)
            anchor = request.GET.get('m', 0)
    except Exception, ex:
        location_obj = ''
        anchor = 0
        print ex
    interest_type_list = DMPDict.objects.filter(isUsed=1, dictType='兴趣分类').order_by("dictId")
    return render(request, "locatedit.html", {'interest_type_list': interest_type_list,
                                              'location_obj': location_obj, 'anchor': anchor})


"""
    标签管理 - 位置信息 [编辑-保存]
"""


def locations_update(request):
    try:
        if request.method == 'POST':
            locat_obj = LocationInfo.objects.get(id=request.POST['locationId'])
            locat_obj.locationStage = request.POST['locationStage']
            locat_obj.locationInterest = request.POST['locationInterest']

            locat_obj.save()
            result = "success"
        else:
            result = "error"
    except Exception, ex:
        print ex
        result = "error"
    messages.success(request, result)
    return HttpResponseRedirect("/dmp/locations/#" + request.POST['m'])


""" 标签管理 - 广告信息 """


def ads_main(request):
    return render(request, "adsinfo.html")


""" 标签管理 - 兴趣映射 """


def interest_main(request):
    page = 1
    page_multi = 1
    search = ''
    try:
        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            page_multi = int(request.GET.get('pageMulti', '1'))
            search = request.GET.get('q', '')
            if page < 1:
                page = 1
        if request.method == 'POST':
            search = str(request.POST['q'])
    except:
        page = 1
        page_multi = 1
        search = ''

    channel_list = ChannelInterest.objects.filter(isUsed=1).order_by("chnId", "chnName")
    if len(search) > 0:
        channel_list = channel_list.filter(cId__in=search.split(","))

    paginator = Paginator(channel_list, 15)
    try:
        channel_page = paginator.page(page)
    except PageNotAnInteger:
        channel_page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        channel_page = paginator.page(paginator.num_pages)

    has_next = True
    # 总页数大于需要显示的页数
    if one_page_num * page_multi <= paginator.num_pages:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, page_multi * one_page_num + 1)
    else:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, paginator.num_pages + 1)
        has_next = False
    return render(request, 'interestinfo.html', {'channel': channel_page, 'page_curt_range': page_curt_range,
                                                 'search_value': search, 'pageMulti': page_multi,
                                                 'one_page_num': one_page_num, 'has_next': has_next})


""" 标签管理 - 兴趣映射 - 编辑 """


def interest_edit(request):
    try:
        if request.method == 'GET':
            page = request.GET.get("p", 1)
            pagemulit = request.GET.get("pm", 1)
            search_value = request.GET.get('q', 1)
            channel_obj = ChannelInterest.objects.filter(isUsed=1).get(id=request.GET.get("id", None))
        else:
            pass
    except Exception, ex:
        page = 1
        pagemulit = 1
        search_value = ''
        print ex
    interest_type_list = DMPDict.objects.filter(isUsed=1, dictType='兴趣分类').order_by("dictId")
    return render(request, "interestedit.html", {'interest_type_list': interest_type_list, 'page': page,
                                                 'pageMulti': pagemulit, 'search_value': search_value,
                                                 'chn_obj': channel_obj})


""" 标签管理 - 兴趣映射 - 提交 """


def interest_update(request):
    try:
        if request.method == 'POST':
            search_value = request.POST['q']
            page = int(request.POST['page'])
            pageMulti = int(request.POST['pageMulti'])

            chn_obj = ChannelInterest.objects.get(id=request.POST['id'])
            chn_obj.chnStage = request.POST['chnStage']
            chn_obj.chnInterest = request.POST['chnInterest']
            chn_obj.save()
            result = "success"
    except Exception, ex:
        result = "error"
        page = 1
        pageMulti = 1
        search_value = ''
        print ex
    messages.success(request, result)
    return HttpResponseRedirect("/dmp/interest/?page=" + str(page) + "&&pageMulti=" + str(pageMulti) + "&&q=" + str(
        search_value))
