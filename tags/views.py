# coding: utf-8
import json, urllib, time, os, zipfile, shutil
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from tags.models import APPInfo, DMPDict, PhoneInfo, LocationInfo, ChannelInterest, StructHuman


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


# Create your views here.
one_page_num = 15
ISOTIMEFORMAT='%Y-%m-%d %X'
ELASTICSEARCHSERVER = 'http://58.61.152.2:9210/_sql?sql='

## APP查询
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


##  APP编辑
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


##  APP更新
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
            appInfo_obj.appAge = request.POST['appAge']
            appInfo_obj.appMedium = request.POST['appMedium']
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


##  手机标注 - 列表页
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


##  手机编辑
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


## 手机编辑 - 保存
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


## 人群构建
def struct_people_main(request):
    app_type_list = DMPDict.objects.filter(isUsed=1, dictType='APP类别').order_by("dictId")
    interest_type_list = DMPDict.objects.filter(isUsed=1, dictType='兴趣分类').order_by("dictId")
    often_place_list = DMPDict.objects.filter(isUsed=1, dictType='常去地点').order_by("dictId")
    prov_city_list = DMPDict.objects.filter(isUsed=1, dictType='省市').order_by("dictId")
    chnl_used_list = DMPDict.objects.filter(isUsed=1, dictType='渠道').order_by("dictId")

    return render(request, "structpeople.html", {"app_type_list": app_type_list,
                                                 "interest_type_list": interest_type_list,
                                                 "often_place_list": often_place_list,
                                                 "prov_city_list": prov_city_list,
                                                 "chnl_used_list": chnl_used_list})


## 人群构建 - 保存
def save_struct_condition(request):
    mssg = {'message': '保存成功啦!'}
    if request.method == 'POST':
        humanName = request.POST['humanName']
        humanDesc = request.POST['humanDesc']
        human = StructHuman.objects.create(name=humanName, desc=humanDesc)

        if request.POST['humanCondition']:
            human.search = request.POST['humanCondition']
        else:
            human.search = "*"
        human.updateSql = str(request.POST['humanUpdateCdt']).replace("'","\\'")
        human.humanCount = request.POST['humanCount']
        human.humanFlux = request.POST['humanFlux']
        human.updateTime = time.strftime(ISOTIMEFORMAT,time.localtime())
        human.save()
    else:
        mssg = {'message': '保存失败啦!'}
    return JsonResponse(mssg)


##  标签管理 - 位置信息
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


## 标签管理 - 位置信息 [编辑]
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


##  标签管理 - 位置信息 [编辑-保存]
def locations_update(request):
    try:
        if request.method == 'POST':
            locat_obj = LocationInfo.objects.get(id=request.POST['locationId'])
            locat_obj.locationStage = request.POST['locationStage']
            locat_obj.locationInterest = request.POST['locationInterest']
            locat_obj.locationAge = request.POST['locationAge']

            locat_obj.save()
            result = "success"
        else:
            result = "error"
    except Exception, ex:
        print ex
        result = "error"
    messages.success(request, result)
    return HttpResponseRedirect("/dmp/locations/#" + request.POST['m'])


## 标签管理 - 广告信息
def ads_main(request):
    return render(request, "adsinfo.html")


## 标签管理 - 兴趣映射
def interest_main(request):
    page = 1
    page_multi = 1
    search = ''
    search_cname = ''
    try:
        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            page_multi = int(request.GET.get('pageMulti', '1'))
            search = request.GET.get('q', '')
            search_cname = request.GET.get('cname', '')
            if page < 1:
                page = 1
        if request.method == 'POST':
            search = str(request.POST['q'])
            search_cname = request.POST['cname']
    except:
        page = 1
        page_multi = 1
        search = ''
        search_cname = ''

    channel_list = ChannelInterest.objects.filter(isUsed=1).order_by("cId", "chnId")
    if len(search) > 0:
        tmpsearch = search.replace("M", "1000").replace("99", "00")
        channel_list = channel_list.filter(cId__in=tmpsearch.split(","))
    if len(search_cname) > 0:
        channel_list = channel_list.filter(chnName__contains=search_cname)

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
                                                 'search_value': search, 'search_cname': search_cname,'pageMulti': page_multi,
                                                 'one_page_num': one_page_num, 'has_next': has_next})


##   标签管理 - 兴趣映射 - 编辑
def interest_edit(request):
    try:
        if request.method == 'GET':
            page = request.GET.get("p", 1)
            pagemulit = request.GET.get("pm", 1)
            search_value = request.GET.get('q', 1)
            search_cname = request.GET.get('cname', '')
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
                                                 'pageMulti': pagemulit, 'search_value': search_value, 'search_cname': search_cname,
                                                 'chn_obj': channel_obj})


##  标签管理 - 兴趣映射 - 提交
def interest_update(request):
    try:
        if request.method == 'POST':
            search_value = request.POST['q']
            search_cname = request.POST['cname']
            page = int(request.POST['page'])
            pageMulti = int(request.POST['pageMulti'])

            chn_obj = ChannelInterest.objects.get(id=request.POST['id'])
            chn_obj.chnStage = request.POST['chnStage']
            chn_obj.chnInterest = request.POST['chnInterest']
            chn_obj.chnSex = request.POST['chnSex']
            chn_obj.chnAge = request.POST['chnAge']
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
        search_value)+"&&cname="+search_cname)


## 人群分析
def human_analyse(request):
    page = 1
    page_multi = 1
    searchContent = ''
    try:
        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            page_multi = int(request.GET.get('pageMulti', '1'))
            searchContent = request.GET.get('hmName', '')
            if page < 1:
                page = 1
        if request.method == 'POST':
            searchContent = request.POST['hmName']
    except:
        page = 1
        page_multi = 1

    human_analyse_list = StructHuman.objects.all().order_by("-id")
    if len(searchContent) > 0:
        human_analyse_list = human_analyse_list.filter(name__contains=searchContent)

    paginator = Paginator(human_analyse_list, 15)
    try:
        human_analyse_page = paginator.page(page)
    except PageNotAnInteger:
        human_analyse_page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        human_analyse_page = paginator.page(paginator.num_pages)

    has_next = True
    # 总页数大于需要显示的页数
    if one_page_num * page_multi <= paginator.num_pages:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, page_multi * one_page_num + 1)
    else:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, paginator.num_pages + 1)
        has_next = False
    return  render(request, "humananalyse.html", {'humans': human_analyse_page, 'page_curt_range': page_curt_range,
                                             'search_value': searchContent, 'pageMulti': page_multi, 'one_page_num': one_page_num,
                                             'has_next': has_next});

## 删除操作
def human_delete(request):
    page = 1
    page_multi = 1
    searchContent = ''
    try:
        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            page_multi = int(request.GET.get('pageMulti', '1'))
            searchContent = request.GET.get('hmName', '')
            StructHuman.objects.get(id=request.GET.get('id', '')).delete()
            if page < 1:
                page = 1
            else:
                pass
    except:
        page = 1
        page_multi = 1

    human_analyse_list = StructHuman.objects.all().order_by("-id")
    if len(searchContent) > 0:
        human_analyse_list = human_analyse_list.filter(name__contains=searchContent)

    paginator = Paginator(human_analyse_list, 15)
    try:
        human_analyse_page = paginator.page(page)
    except PageNotAnInteger:
        human_analyse_page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        human_analyse_page = paginator.page(paginator.num_pages)

    has_next = True
    # 总页数大于需要显示的页数
    if one_page_num * page_multi <= paginator.num_pages:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, page_multi * one_page_num + 1)
    else:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, paginator.num_pages + 1)
        has_next = False
    return render(request, "humananalyse.html", {'humans': human_analyse_page, 'page_curt_range': page_curt_range,
                                                 'search_value': searchContent, 'pageMulti': page_multi,
                                                 'one_page_num': one_page_num,
                                                 'has_next': has_next});

## 更新
def human_update(request):
    page = 1
    page_multi = 1
    searchContent = ''
    try:
        if request.method == 'GET':
            page = int(request.GET.get('page', '1'))
            page_multi = int(request.GET.get('pageMulti', '1'))
            searchContent = request.GET.get('hmName', '')

            shuman = StructHuman.objects.get(id=request.GET.get('id', ''))
            shuman.humanCount = request.GET.get('tc', '0')
            shuman.humanFlux = request.GET.get('lc', '0')
            shuman.updateTime = time.strftime(ISOTIMEFORMAT,time.localtime())
            shuman.save()
            if page < 1:
                page = 1
            else:
                pass
    except:
        page = 1
        page_multi = 1

    human_analyse_list = StructHuman.objects.all().order_by("-id")
    if len(searchContent) > 0:
        human_analyse_list = human_analyse_list.filter(name__contains=searchContent)

    paginator = Paginator(human_analyse_list, 15)
    try:
        human_analyse_page = paginator.page(page)
    except PageNotAnInteger:
        human_analyse_page = paginator.page(1)
    except (EmptyPage, InvalidPage):
        human_analyse_page = paginator.page(paginator.num_pages)

    has_next = True
    # 总页数大于需要显示的页数
    if one_page_num * page_multi <= paginator.num_pages:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, page_multi * one_page_num + 1)
    else:
        page_curt_range = range((page_multi - 1) * one_page_num + 1, paginator.num_pages + 1)
        has_next = False
    return render(request, "humananalyse.html", {'humans': human_analyse_page, 'page_curt_range': page_curt_range,
                                                 'search_value': searchContent, 'pageMulti': page_multi,
                                                 'one_page_num': one_page_num,
                                                 'has_next': has_next});

def human_export(request):
    if request.method == "GET":
        humanObj = StructHuman.objects.get(id=request.GET.get("id"))
        sql = "SELECT IMEI,IMEIMD5,MAC,PUID FROM test2"
        if not humanObj.search.__eq__("*"):
            sql += " WHERE "+humanObj.search
        else:
            pass
        result = urllib.urlopen(ELASTICSEARCHSERVER+sql)
        result_jsons =json.loads(result.read())["hits"]["hits"]
        data_imei = []
        data_imeimd5 = []
        data_mac = []
        data_puid = []
        for k in result_jsons:
            if str(k["_source"]["IMEI"]).strip():
                data_imei.append(k["_source"]["IMEI"])
            if str(k["_source"]["IMEIMD5"]).strip():
                data_imeimd5.append(k["_source"]["IMEIMD5"])
            if str(k["_source"]["MAC"]).strip():
                data_mac.append(k["_source"]["MAC"])
            if str(k["_source"]["PUID"]):
                data_puid.append(k["_source"]["PUID"])

        if len(data_imei)>0 or len(data_imeimd5)>0 or len(data_mac)>0 or len(data_puid)>0:
            try:
                dirname = "downloadzip/zip"+str(humanObj.id)
                if os.path.exists(dirname):
                    shutil.rmtree(dirname)
                os.makedirs(dirname)
            except OSError, osr:
                pass

            if len(data_imei)>0:
                imei_file_name = "/%s.txt" % str("IMEI")
                imei_file = open(dirname+imei_file_name, 'w')
                for imei in data_imei:
                    imei_file.write(str(imei)+"\n")
                imei_file.close()

            if len(data_imeimd5) > 0:
                imeimd5_file_name = "/%s.txt" % str("IMEIMD5")
                imeimd5_file = open(dirname + imeimd5_file_name, 'w')
                for imeiMD5 in data_imeimd5:
                    imeimd5_file.write(str(imeiMD5) + "\n")
                imeimd5_file.close()

            if len(data_mac) > 0:
                mac_file_name = "/%s.txt" % str("MAC")
                mac_file = open(dirname + mac_file_name, 'w')
                for mac in data_mac:
                    mac_file.write(str(mac) + "\n")
                mac_file.close()

            if len(data_puid) > 0:
                puid_file_name = "/%s.txt" % str("PUID")
                puid_file = open(dirname+ puid_file_name, 'w')
                for puid in data_puid:
                    puid_file.write(str(puid) + "\n")
                puid_file.close()
        else:
            pass

        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))

        zipFileName = "downloadzip/"+ humanObj.name+".zip"
        zf = zipfile.ZipFile(zipFileName, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            zf.write(tar, arcname)
        zf.close()

        def file_iterator(file_name, chunk_size=512):
            with open(file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(zipFileName))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename={0}.zip'.format(humanObj.name)

    return response


def human_show_chart(request):
    if request.method == "GET":
        humanObj = StructHuman.objects.get(id=request.GET.get("id"))
        elastic_condition = humanObj.search
        elastic_condition = elastic_condition.replace(">0", ":*").replace("'", "").replace("=", ":")

        dict_all_data = DMPDict.objects.filter(isUsed=1)
        transprarent = elastic_condition.replace("*", "全部")\
            .replace("gender", "性别")\
            .replace("age","年龄")\
            .replace("lfstage","人生阶段")\
            .replace("flow", "流量")\
            .replace("keys", "关键字")\
            .replace("app", "应用名称")\
            .replace("category","应用类别")\
            .replace("client", "操作系统")\
            .replace("network", "联网方式")\
            .replace("isp", "运营商")\
            .replace("price","价格")\
            .replace("brand","品牌")\
            .replace("city","城市")\
            .replace("province","省")\
            .replace("channel","渠道")\
            .replace("inst","兴趣爱好")\
            .replace("instOneLev","一级兴趣爱好")\
            .replace("location","常去地点")\
            .replace("locOneLev","一级常去地点")

        for d in dict_all_data:
            transprarent = transprarent.replace(d.dictId, d.dictName)

        qudaoList = {}
        for qd in DMPDict.objects.filter(dictType='渠道'):
            qudaoList[qd.dictId+"0000"] = qd.dictName
        qudaoMap = json.dumps(qudaoList)

        meijieList = {}
        for mj in DMPDict.objects.order_by("dictId").filter(dictType='媒介'):
            meijieList[mj.dictId]= mj.dictName
        meijieMap = json.dumps(meijieList)

        adViewList = {}
        for ad in DMPDict.objects.order_by("dictId").filter(dictType='广告形式'):
            adViewList[ad.dictId] = ad.dictName
        adviewMap = json.dumps(adViewList)

    else:
        pass
    return  render(request, "humanshowchart.html",{
        "elastic_condition": elastic_condition,
        "qudaoMap": qudaoMap,
        "meijieMap": meijieMap,
        "adviewMap": adviewMap,
        "transprarent": transprarent
    })