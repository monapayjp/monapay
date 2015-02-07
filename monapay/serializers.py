# -*- coding: utf-8 -*-

from django.forms import widgets
from rest_framework import serializers
from monapay.models import Item, Data, Invoice


class ItemRequestSerializer(serializers.Serializer):
    label = serializers.CharField(required=True, max_length=128) 


    def validate_label(self, attrs, source):
        def _validate_data(item):
            if item.data.status == Data.PRIVATE:
                raise serializers.ValidationError(
                    "The specified item is now in private")
            elif item.data.status == Data.SUSPENSION:
                raise serializers.ValidationError(
                    "The specified item is suspended")

        value = attrs[source]
        queryset = Item.objects.filter(label=value)
        if not queryset.exists():
            raise serializers.ValidationError(
                "The specified item does not exist")
        item = Item.objects.get(label=value)
        self._item = item
        if item.item_type == Item.DATA:
            _validate_data(item)
        return attrs


class DataSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(source="natural_price")
    pub_date = serializers.DecimalField(source="item.pub_date")

    class Meta:
        model = Data
        fields = ("title", "description", "price", "pub_date")


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ("title", "description", "price", "admin_address",
                  "pos_data", "redirect_url", "notification_url",
                  "notification_email")
