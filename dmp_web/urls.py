"""dmp_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import tags.views as dmp

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dmp/appsinfo/$', dmp.appsinfo_main),
    url(r'^dmp/appsinfo/edit/$', dmp.app_edit),
    url(r'^dmp/appsinfo/update/$', dmp.app_update),

    url(r'^dmp/phoneinfo/$', dmp.phoneinfo_main),
    url(r'^dmp/phoneinfo/edit/$', dmp.phone_edit),
    url(r'^dmp/phoneinfo/update/$', dmp.phone_update),

    url(r'^dmp/structmans/$', dmp.struct_people_main),

    url(r'^dmp/locations/$', dmp.locations_main),
    url(r'^dmp/locations/edit/$', dmp.locations_edit),
    url(r'^dmp/locations/update/$', dmp.locations_update),

    url(r'^dmp/ads/$', dmp.ads_main),
    url(r'^dmp/interest/$', dmp.interest_main),
]
