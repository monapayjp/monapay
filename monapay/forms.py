# -*- coding: utf-8 -*-

import logging
import socket
from decimal import Decimal
from django import forms
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from monapay.rpc import make_rpc_connection, get_minconf

logger = logging.getLogger(__name__)

class BaseItemForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    description = forms.CharField(
        max_length=1000, widget=forms.Textarea, required=False)
    secret_link = forms.URLField(max_length=256, required=True)
    price = forms.DecimalField(
        max_digits=8, decimal_places=3, required=True,
        validators=[
            MinValueValidator(settings.PAYMENT_MINIMUM_PRICE),
            MaxValueValidator(settings.PAYMENT_MAXIMUM_PRICE)])


class EditItemForm(BaseItemForm):
    pub_flag = forms.BooleanField(initial=False, required=False)


class CreateItemForm(BaseItemForm):
    admin_address = forms.CharField(max_length=128, required=True)
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        error_messages={'required': _("You must agree to the terms.")})

    def clean_admin_address(self):
        # check the connection
        address = self.cleaned_data["admin_address"]
        try:
            conn = make_rpc_connection()
            result = conn.validateaddress(address)
            if result.isvalid:
                return address
            else:
                raise forms.ValidationError(_("Invalid address specified."))
        except socket.error, msg:
            logger.error("RPC connection refused.")
            raise forms.ValidationError(_("Internal server error occurred. Please try it again after a few hours."))


class BaseInvoiceForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    description = forms.CharField(
        max_length=1000, widget=forms.Textarea, required=False)
    price = forms.DecimalField(
        max_digits=8, decimal_places=3, required=True,
        validators=[
            MinValueValidator(settings.PAYMENT_MINIMUM_PRICE),
            MaxValueValidator(settings.PAYMENT_MAXIMUM_PRICE)])
    pos_data = forms.CharField(max_length=200, required=False)
    redirect_url = forms.URLField(max_length=256, required=False)
    notification_url = forms.URLField(max_length=256, required=False)
    notification_email = forms.EmailField(max_length=256, required=False)


class EditInvoiceForm(BaseInvoiceForm):
    pub_flag = forms.BooleanField(initial=False, required=False)


class CreateInvoiceForm(BaseInvoiceForm):
    admin_address = forms.CharField(max_length=128, required=True)
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        error_messages={'required': _("You must agree to the terms.")})

    def clean_admin_address(self):
        # check the connection
        address = self.cleaned_data["admin_address"]
        try:
            conn = make_rpc_connection()
            result = conn.validateaddress(address)
            if result.isvalid:
                return address
            else:
                raise forms.ValidationError(_("Invalid address specified."))
        except socket.error, msg:
            logger.error("RPC connection refused.")
            raise forms.ValidationError(_("Internal server error occurred. Please try it again after a few hours."))


class PaymentForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item', None)
        self.wallet = kwargs.pop('wallet', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        try:
            conn = make_rpc_connection()
            minconf = get_minconf(self.item.data.natural_price())
            received = conn.getreceivedbyaddress(
                self.wallet.address, minconf=minconf)
            if received == 0.0:
                raise forms.ValidationError(
                    _('It seems that your transaction does not spread an entire network.' \
                    ' Please click "Confirm Payment" button after a few minutes' \
                    ' ({minconf} confirmations are required).').format(minconf=minconf))
            elif received < self.item.data.natural_price():
                balance = (self.item.data.natural_price() - received).normalize()
                error_text = _("{0:f} MONA is required to purchase this product.")
                raise forms.ValidationError(error_text.format(balance))
            return super(PaymentForm, self).clean()
        except socket.error, msg:
            logger.error("RPC connection refused.")
            raise forms.ValidationError(_("Internal server error occurred. Please try it again after a few hours."))
