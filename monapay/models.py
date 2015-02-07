# -*- coding: utf-8 -*-

from django.db import models
from monapay.currency import render_natural_unit, atomic_to_natural_unit

# Create your models here.
class Item(models.Model):
    label = models.CharField(max_length=128, db_index=True, unique=True)
    secret_key = models.CharField(max_length=128, db_index=True, unique=True)

    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, editable=False)

    DONATION = "Donation"
    DATA = "Data"
    INVOICE = "Invoice"
    PRODUCT = "Product"
    ITEM_TYPE_CHOICES = (
        (DONATION, "Donation"),
        (DATA, "Data"),
        (INVOICE, "Invoice"),
        (PRODUCT, "Product"),
    )
    item_type = models.CharField(
        max_length=128, choices=ITEM_TYPE_CHOICES, default=DATA)
    
    def __unicode__(self):
        if self.item_type == Item.DATA:
            return u"{0} ({1})".format(self.data.title, self.label)
        else:
            return u"OTHER ({1})".format(self.label)


class Data(models.Model):
    item = models.OneToOneField(Item, related_name="data", primary_key=True)

    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    price = models.BigIntegerField(default=0)
    admin_address = models.CharField(max_length=128, blank=False)
    secret_link = models.URLField(max_length=256, blank=True)
    max_limit = models.PositiveIntegerField(default=0)

    PUBLIC = "Public"
    PRIVATE = "Private"
    SUSPENSION = "Suspension"
    STATUS_CHOICES = (
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
        (SUSPENSION, "Suspension"),
    )
    status = models.CharField(
        max_length=128, choices=STATUS_CHOICES, default=PUBLIC)

    def render_price(self):
        return u"{0} MONA".format(render_natural_unit(self.price))

    def natural_price(self):
        return atomic_to_natural_unit(self.price)


class Invoice(models.Model):
    item = models.OneToOneField(Item, related_name="invoice", primary_key=True)

    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    price = models.BigIntegerField(default=0)
    admin_address = models.CharField(max_length=128, blank=False)
    pos_data = models.CharField(max_length=200, blank=True)
    redirect_url = models.URLField(max_length=256, blank=True)
    notification_url = models.URLField(max_length=256, blank=True)
    notification_email = models.EmailField(max_length=256, blank=True)


class Wallet(models.Model):
    address = models.CharField(max_length=128)
    wallet_label = models.CharField(max_length=128, db_index=True)
    item = models.ForeignKey(Item, related_name="wallets")

    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, editable=False)

    UNPAID = "Unpaid"
    PAID = "Paid"
    SUSPENSION = "Suspension"
    PAYMENT_STATUS_CHOICES = (
        (UNPAID, "Unpaid"),
        (PAID, "Paid"),
        (SUSPENSION, "Suspension"),
    )
    payment_status = models.CharField(
        max_length=64, choices=PAYMENT_STATUS_CHOICES,
        default=UNPAID, db_index=True)

    def __unicode__(self):
        return self.address


class PaymentTransaction(models.Model):
    wallet = models.OneToOneField(Wallet, primary_key=True)
    address = models.CharField(max_length=128)
    item = models.ForeignKey(Item, related_name="transactions")
    total = models.BigIntegerField()
    send_amount = models.BigIntegerField(default=0)
    fee_amount = models.BigIntegerField(default=0)
    transaction_fee = models.BigIntegerField(default=0)
    transaction_id = models.CharField(
        max_length=128, blank=True, default="")
    
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, editable=False)

    UNPROCESSED = "Unprocessed"
    PROCESSED = "Processed"
    STATUS_CHOICES = (
        (UNPROCESSED, "Unprocessed"),
        (PROCESSED, "Processed"),
    )
    status = models.CharField(
        max_length=64, choices=STATUS_CHOICES,
        default=UNPROCESSED, db_index=True)

    def __unicode__(self):
        return self.transaction_id
