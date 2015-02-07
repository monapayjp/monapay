# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'monapay_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
            ('secret_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('item_type', self.gf('django.db.models.fields.CharField')(default='Data', max_length=128)),
        ))
        db.send_create_signal(u'monapay', ['Item'])

        # Adding model 'Data'
        db.create_table(u'monapay_data', (
            ('item', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['monapay.Item'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('admin_address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('secret_link', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('max_limit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Public', max_length=128)),
        ))
        db.send_create_signal(u'monapay', ['Data'])

        # Adding model 'Wallet'
        db.create_table(u'monapay_wallet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('wallet_label', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wallets', to=orm['monapay.Item'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('payment_status', self.gf('django.db.models.fields.CharField')(default='Unpaid', max_length=64, db_index=True)),
        ))
        db.send_create_signal(u'monapay', ['Wallet'])

        # Adding model 'PaymentTransaction'
        db.create_table(u'monapay_paymenttransaction', (
            ('wallet', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['monapay.Wallet'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['monapay.Item'])),
            ('total', self.gf('django.db.models.fields.BigIntegerField')()),
            ('send_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('fee_amount', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('transaction_fee', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unprocessed', max_length=64, db_index=True)),
        ))
        db.send_create_signal(u'monapay', ['PaymentTransaction'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'monapay_item')

        # Deleting model 'Data'
        db.delete_table(u'monapay_data')

        # Deleting model 'Wallet'
        db.delete_table(u'monapay_wallet')

        # Deleting model 'PaymentTransaction'
        db.delete_table(u'monapay_paymenttransaction')


    models = {
        u'monapay.data': {
            'Meta': {'object_name': 'Data'},
            'admin_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['monapay.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'max_limit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'secret_link': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Public'", 'max_length': '128'}),
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