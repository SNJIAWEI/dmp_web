# coding: utf-8
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from tags.models import APPInfo, DMPDict, PhoneInfo

# Create your views here.
one_page_num = 15

""" APP查询 """
def appsinfo(request):
    try:
        page = int(request.GET.get('page', '1'))
        page_multi = int(request.GET.get('pageMulti', '1'))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
        page_multi = 1

    apps_list = APPInfo.objects.filter(appUsed=1).order_by("id")
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
        page_curt_range = range((page_multi - 1)*one_page_num+1, page_multi*one_page_num+1)
    else:
        page_curt_range = range((page_multi - 1)*one_page_num+1, paginator.num_pages+1)
        has_next = False
    return render(request, 'appsinfo.html', {'apps': apps_page, 'page_curt_range': page_curt_range,
                                             'pageMulti': page_multi, 'one_page_num': one_page_num, 'has_next': has_next})

""" APP编辑 """
def app_edit(request):
    try:
        page = request.GET.get("p", 1)
        pagemulit = request.GET.get("pm", 1)
        if request.GET.get("id", None):
            app_obj = APPInfo.objects.filter(appUsed=1).get(id=request.GET.get("id", None))
    except:
        pass
    return render(request, "appsedit.html", {'app': app_obj, 'page': page, 'pageMulti': pagemulit})

""" APP更新 """
def app_update(request):
    if request.method == 'POST':
        try:
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
    return HttpResponseRedirect("/dmp/appsinfo/?page="+str(page)+"&&pageMulti="+str(pageMulti))


""" 手机标注 - 列表页 """
def phone_list(request):
    try:
        page = int(request.GET.get('page', '1'))
        page_multi = int(request.GET.get('pageMulti', '1'))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
        page_multi = 1

    telphone_list = PhoneInfo.objects.filter(isUsed=1).order_by("id")
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
                                             'pageMulti': page_multi, 'one_page_num': one_page_num, 'has_next': has_next})

""" 手机编辑 """
def phone_edit(request):
    try:
        page = request.GET.get("p", 1)
        pagemulit = request.GET.get("pm", 1)
        if request.GET.get("id", None):
            phone_obj = PhoneInfo.objects.filter(isUsed=1).get(id=request.GET.get("id", None))
    except:
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


def struct_people(request):
    app_type_list = DMPDict.objects.filter(isUsed=1, dictType='APP类别').order_by("dictId")
    interest_type_list = DMPDict.objects.filter(isUsed=1, dictType='兴趣分类').order_by("dictId")

    tree_xq_dict = {}
    tree_xq_node_dict = {}
    for itl in interest_type_list:
        if len(itl.dictId) == 5:
            tree_xq_dict[itl.dictId] = '{id: "%s", pId: 0, name: "%s", open: false, children:[temp_children]},' % (itl.dictId, itl.dictName)
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
    return render(request, "structpeople.html",{"app_type_list": app_type_list, "interest_type_dict": tree_xq_dict})