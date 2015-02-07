# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('monapay.urls')),
    url(r'^payment_manage/', include(admin.site.urls)),
)
