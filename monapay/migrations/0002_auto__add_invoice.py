# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table(u'monapay_invoice', (
            ('item', self.gf('django.db.models.fields.related.OneToOneField')(related_name='invoice', unique=True, primary_key=True, to=orm['monapay.Item'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('admin_address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pos_data', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('redirect_url', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('notification_url', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('notification_email', self.gf('django.db.models.fields.EmailField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'monapay', ['Invoice'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table(u'monapay_invoice')


    models = {
        u'monapay.data': {
            'Meta': {'object_name': 'Data'},
            'admin_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'data'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['monapay.Item']"}),
            'max_limit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'secret_link': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Public'", 'max_length': '128'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'monapay.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'admin_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'invoice'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['monapay.Item']"}),
            'notification_email': ('django.db.models.fields.EmailField', [], {'max_length': '256', 'blank': 'True'}),
            'notification_url': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'pos_data': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'price': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'redirect_url': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'monapay.item': {
            'Meta': {'object_name': 'Item'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'Data'", 'max_length': '128'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'secret_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        u'monapay.paymenttransaction': {
            'Meta': {'object_name': 'PaymentTransaction'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'fee_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': u"orm['monapay.Item']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'send_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unprocessed'", 'max_length': '64', 'db_index': 'True'}),
            'total': ('django.db.models.fields.BigIntegerField', [], {}),
            'transaction_fee': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'wallet': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['monapay.Wallet']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'monapay.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wallets'", 'to': u"orm['monapay.Item']"}),
            'payment_status': ('django.db.models.fields.CharField', [], {'default': "'Unpaid'", 'max_length': '64', 'db_index': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'wallet_label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        }
    }

    complete_apps = ['monapay']