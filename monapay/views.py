# -*- coding: utf-8 -*-

import logging
import urllib
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView, DetailView
from monapay.currency import (
    natural_to_atomic_unit, atomic_to_natural_unit, quantize_natural_unit)
from monapay.forms import (
    EditItemForm, CreateItemForm, PaymentForm, CreateInvoiceForm)
from monapay.keycode import make_item_key, make_wallet_key, make_secret_key
from monapay.models import Item, Data, Wallet, PaymentTransaction, Invoice
from monapay.rpc import make_rpc_connection, get_minconf

logger = logging.getLogger(__name__)

# Create your views here.
class RPCConnectionMixin(object):

    def __init__(self, *args, **kwargs):
        self._conn = None
        super(RPCConnectionMixin, self).__init__(*args, **kwargs)

    def get_connection(self):
        if self._conn is None:
            self._conn = make_rpc_connection()
            if settings.DEBUG:
                logger.info("monapay makes a connection(total balance={0})".format(self._conn.getbalance()))
            return self._conn
        else:
            return self._conn
    conn = property(get_connection)


class AbsoluteURLMixin(object):
    def build_secure_url(self, url):
        if settings.DEBUG:
            return url
        else:
            return url.replace('http://', 'https://')

    def get_context_data(self, **kwargs):
        context = super(AbsoluteURLMixin, self).get_context_data(**kwargs)
        context["absolute_url"] = self.build_secure_url(
            self.request.build_absolute_uri())
        return context


class PaymentView(RPCConnectionMixin, AbsoluteURLMixin, FormView):
    form_class = PaymentForm

    def make_payment_qrcode(self, address, amount):
        label = u"monapay"
        message = u"Thank you for paying with Monapay"
        return u"monacoin:{0}?amount={1}&label={2}&message={3}".format(
            address, amount, urllib.quote(label), urllib.quote(message))

    def dispatch(self, *args, **kwargs):
        self.item = get_object_or_404(Item, label=kwargs["label"])
        session_label = u"item:{0}".format(self.item.label)
        if session_label in self.request.session:
            self.wallet = Wallet.objects.get(
                pk=self.request.session[session_label])
            if self.wallet.payment_status == Wallet.PAID:
                return redirect('payment_done', label=self.wallet.wallet_label)
        else:
            with transaction.atomic():
                new_wallet = Wallet.objects.create(
                    address="", wallet_label="", item=self.item)
                new_pk = new_wallet.pk
                new_address = self.conn.getnewaddress(account=str(new_pk))
                new_wallet.address = new_address
                new_wallet.wallet_label = make_wallet_key(new_pk)
                new_wallet.save()
                self.wallet = new_wallet
                self.request.session[session_label] = self.wallet.pk
        return super(PaymentView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PaymentView, self).get_form_kwargs()
        kwargs["item"] = self.item
        kwargs["wallet"] = self.wallet
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["qrcode"] = self.make_payment_qrcode(
            self.wallet.address, self.item.data.natural_price())
        context["item"] = self.item
        context["wallet"] = self.wallet
        return context

    def form_valid(self, form):
        minconf = get_minconf(self.item.data.natural_price())
        received = self.conn.getreceivedbyaddress(
            self.wallet.address, minconf=minconf)

        logger.info("begin transaction(addr={0}, received={1}, minconf={2})".format(
            self.wallet.address, received, minconf))

        with transaction.atomic():
            self.wallet.payment_status = Wallet.PAID
            self.wallet.save()
            payment = PaymentTransaction.objects.create(
                wallet=self.wallet, address=self.item.data.admin_address,
                item=self.item, total=natural_to_atomic_unit(received))

        R = 1 - settings.PAYMENT_DEFAULT_FEE
        send_amount = quantize_natural_unit(received * R)
        transaction_id = self.conn.sendfrom(
            str(self.wallet.pk), self.item.data.admin_address,
            float(send_amount), minconf=minconf)

        logger.info("payment succeed(addr={0}, id={1})".format(
            self.wallet.address, transaction_id))

        transaction_body = self.conn.gettransaction(transaction_id)
        residual = received + transaction_body.amount + transaction_body.fee
        #self.conn.setaccount(self.wallet.address, settings.PAYMENT_FEE_ACCOUNT_NAME)
        if residual > 0:
            self.conn.move(str(self.wallet.pk), settings.PAYMENT_FEE_ACCOUNT_NAME,
                float(residual), minconf=minconf)
        elif residual < 0:
            logger.error("residual has a negative number!(addr={0}, residual={1})".format(
                self.wallet.address, residual))

        payment.send_amount = natural_to_atomic_unit(-transaction_body.amount)
        payment.fee_amount = natural_to_atomic_unit(residual)
        payment.transaction_fee = natural_to_atomic_unit(-transaction_body.fee)
        payment.transaction_id = transaction_id
        payment.status = PaymentTransaction.PROCESSED
        payment.save()

        logger.info("end transaction(addr={0})".format(self.wallet.address))
        return super(PaymentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("payment_done", kwargs={"label": self.wallet.wallet_label})


class PaymentSuccessView(DetailView):
    model = Wallet

    def dispatch(self, *args, **kwargs):
        self.wallet = get_object_or_404(Wallet, wallet_label=self.kwargs["label"])
        if self.wallet.payment_status == Wallet.UNPAID:
            raise Http404
        return super(PaymentSuccessView, self).dispatch(*args, **kwargs)

    def get_object(self, **kwargs):
        return self.wallet

    def get_context_data(self, **kwargs):
        context = super(PaymentSuccessView, self).get_context_data(**kwargs)
        context["item"] = self.wallet.item
        return context


class CreateItemView(FormView):
    form_class = CreateItemForm

    def form_valid(self, form):
        atomic_price = natural_to_atomic_unit(form.cleaned_data["price"])
        with transaction.atomic():
            new_pk = Item.objects.all().count() + 1
            self.label = make_item_key(new_pk)
            self.secret_key = make_secret_key(new_pk)
            new_item = Item.objects.create(
                label=self.label,
                secret_key=self.secret_key,
                item_type=Item.DATA)
            new_data_link = Data.objects.create(item=new_item,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                price=atomic_price,
                admin_address=form.cleaned_data["admin_address"],
                max_limit=0,
                secret_link=form.cleaned_data["secret_link"])

        return super(CreateItemView, self).form_valid(form)

    def get_success_url(self):
        return reverse("create_item_done", kwargs={"secret_key": self.secret_key})


class SecretItemMixin(object):
    def dispatch(self, *args, **kwargs):
        self.item = get_object_or_404(Item, secret_key=self.kwargs["secret_key"])
        return super(SecretItemMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SecretItemMixin, self).get_context_data(**kwargs)
        context["item"] = self.item
        return context


class CreateItemSuccessView(SecretItemMixin, TemplateView):

    def build_secure_url(self, url):
        if settings.DEBUG:
            return url
        else:
            return url.replace('http://', 'https://')

    def get_context_data(self, **kwargs):
        context = super(CreateItemSuccessView, self).get_context_data(**kwargs)
        context["absolute_payment_url"] = self.build_secure_url(
            self.request.build_absolute_uri(
                reverse('payment', kwargs={'label': self.item.label})))
        context["absolute_secret_url"] = self.build_secure_url(
            self.request.build_absolute_uri(
                reverse('edit_item', kwargs={'secret_key': self.item.secret_key})))
        context["absolute_media_url"] = self.build_secure_url(
            self.request.build_absolute_uri(settings.STATIC_URL))
        return context


class EditItemView(SecretItemMixin, FormView):
    form_class = EditItemForm

    def get_initial(self):
        kwargs = super(EditItemView, self).get_initial()
        kwargs["title"] = self.item.data.title
        kwargs["description"] = self.item.data.description
        kwargs["secret_link"] = self.item.data.secret_link
        kwargs["price"] = self.item.data.natural_price()
        return kwargs

    def form_valid(self, form):
        atomic_price = natural_to_atomic_unit(form.cleaned_data["price"])
        self.item.data.title = form.cleaned_data["title"]
        self.item.data.description = form.cleaned_data["description"]
        self.item.data.price = atomic_price
        self.item.data.secret_link = form.cleaned_data["secret_link"]
        if form.cleaned_data["pub_flag"]:
            self.item.data.status = Data.PRIVATE
        self.item.data.save()
        return super(EditItemView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditItemView, self).get_context_data(**kwargs)
        n_visitors = Wallet.objects.filter(item=self.item).count()
        n_purchasers = Wallet.objects.filter(
            item=self.item, payment_status=Wallet.PAID).count()
        achievement_rate = 0.0 if n_visitors == 0 else \
            (float(n_purchasers) / float(n_visitors) * 100)
        context["n_visitors"] = n_visitors
        context["n_purchasers"] = n_purchasers
        context["n_non_purchasers"] = n_visitors - n_purchasers
        context["achievement_rate"] = achievement_rate
        context["non_achievement_rate"] = 100 - achievement_rate
        return context

    def get_success_url(self):
        return reverse("edit_item_done")


class EditItemSuccessView(TemplateView):
    pass


from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from monapay.serializers import InvoiceSerializer, ItemRequestSerializer, DataSerializer

class InvoiceAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ## 概要
    monapayのinvoice APIは、簡易的にmonacoin決済ページを作成するために作られました。
    """
    serializer_class = InvoiceSerializer


class DataAPIView(viewsets.GenericViewSet):
    """
    ## 概要
    `/api/product`はmonapay内のデジタルコンテンツの情報を取得するAPIです．
    これによって，ユーザは対象のデジタルコンテンツのタイトル，紹介文，金額
    などといった詳細な情報を簡単に取得できます．

    ### 製品情報の取得
    取得にはGETリクエストを使用します．必要なパラメータは次の通りです．

    - `label`: 商品のURLの末尾に付与される数桁の英数字．
               具体的には，取得したい商品のURLが
               `https://monapay.com/mona/confirm/1234abcd`
               であった場合，`label`には`1234abcd`を指定します．
    - `format`: 返される結果のフォーマット． `api`, `json`, `xml`の
                いずれかを指定します．指定しない場合のデフォルトは`api`です．
                `api`の場合，リクエスト結果はAPIの結果を確認しやすい
                HTML形式で返されます．

    返されるデータは次の通りです．

    - `title`: 商品のタイトル
    - `description`: 商品の説明文
    - `price`: 商品の価格(単位はMONA)
    - `pub_date`: 商品の発行日(日本時間(JST)でなく、グリニッジ標準時(GMT)
                  で提供されることに注意してください)

    例えば，次のようなURLにアクセスすることで
    商品ラベル`1234abcd`のデータをJSON形式で取得できます．

    ```
    https://monapay.com/api/product/?label=1234abcd&format=json
    ```
    """

    def get_view_name(self):
        return "api/product"

    def retrieve(self, request, *args, **kwargs):
        serializer = ItemRequestSerializer(data=request.GET)
        if serializer.is_valid():
            item = serializer._item
            data_serializer = DataSerializer(item.data)
            return Response(data_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Item.objects.all()
