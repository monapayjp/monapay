# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from monapay.views import (
    PaymentView, PaymentSuccessView,
    CreateItemView, CreateItemSuccessView,
    EditItemView, EditItemSuccessView,
    DataAPIView, InvoiceAPIView)

urlpatterns = patterns('',
    url(r'^$', CreateItemView.as_view(
        template_name='monapay/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(
        template_name='monapay/about.html'), name='about'),
    url(r'^terms/', TemplateView.as_view(
        template_name='monapay/terms.html'), name='terms'),
    # mona urls
    url(r'^mona/success/(?P<secret_key>[0-9a-zA-Z]+)/$',
        CreateItemSuccessView.as_view(
            template_name='monapay/create_item_done.html'),
        name='create_item_done'),
    url(r'^mona/confirm/(?P<label>[0-9a-zA-Z]+)/$',
        PaymentView.as_view(template_name='monapay/payment.html'),
        name='payment'),
    url(r'^mona/payment/(?P<label>[0-9a-zA-Z]+)/$',
        PaymentSuccessView.as_view(
            template_name='monapay/payment_done.html'),
        name='payment_done'),
    url(r'^mona/edit/done/$',
        EditItemSuccessView.as_view(template_name='monapay/edit_item_done.html'),
        name='edit_item_done'),
    url(r'^mona/edit/(?P<secret_key>[0-9a-zA-Z]+)/$',
        EditItemView.as_view(template_name='monapay/edit_item.html'),
        name='edit_item'),
    # APIs
    url(r'^api/product/$', DataAPIView.as_view({"get": "retrieve"})),
#    url(r'^api/invoice/$', InvoiceAPIView.as_view({"post": "create"})),
)
