# -*- coding: utf-8 -*-

from django.contrib import admin
from monapay.models import Item, Data, Wallet, PaymentTransaction

# Register your models here.
class DataInline(admin.StackedInline):
    model = Data
    extra = 0
    max_num = 1

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Item", {
            "fields": ["label", "secret_key", "item_type"]}),
    ]
    list_display = ("label", "secret_key", "item_type", "pub_date")
    list_filter = ("item_type",)
    search_fields = ['label']
    inlines = [ DataInline ]

admin.site.register(Item, ItemAdmin)

def make_published(modeladmin, request, queryset):
    queryset.update(status=Data.PUBLIC)
make_published_short_description = u"Mark selected data items as published"

def make_suspended(modeladmin, request, queryset):
    queryset.update(status=Data.SUSPENSION)
make_suspended_short_description = u"Mark selected data items as suspended"

class DataAdmin(admin.ModelAdmin):
    model = Data
    list_display = ("title", "price", "admin_address", "status", "secret_link")
    actions = [make_published, make_suspended]
    list_filter = ("status",)
    search_fields = ['item__label']

admin.site.register(Data, DataAdmin)

class WalletAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Wallet", {
            "fields": ["item", "address", "wallet_label", "payment_status"]}),
    ]
    list_display = ("pk", "item", "address", "wallet_label", "payment_status", "pub_date")
    list_filter = ("payment_status", )
    
admin.site.register(Wallet, WalletAdmin)

class PaymentTransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("PaymentTransaction", {
            "fields": ["wallet", "address", "item", "total", "send_amount",
                       "fee_amount", "transaction_id", "status"]}),
    ]
    list_display = ("item", "total", "send_amount", "transaction_fee",
                    "fee_amount", "pub_date", "status", "transaction_id")
    list_filter = ("status", )
    search_fields = ['transaction_id']

admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
