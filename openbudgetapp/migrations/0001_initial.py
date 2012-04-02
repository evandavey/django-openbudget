# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Split'
        db.create_table('openbudgetapp_split', (
            ('accountset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.AccountSet'])),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('tx', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Transaction'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Account'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=4)),
        ))
        db.send_create_signal('openbudgetapp', ['Split'])

        # Adding model 'AccountBudget'
        db.create_table('openbudgetapp_accountbudget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Account'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=4)),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('estimated', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pctnondiscrentionary', self.gf('django.db.models.fields.FloatField')(default=1.0)),
        ))
        db.send_create_signal('openbudgetapp', ['AccountBudget'])

        # Adding model 'InflationRate'
        db.create_table('openbudgetapp_inflationrate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=4)),
        ))
        db.send_create_signal('openbudgetapp', ['InflationRate'])

        # Adding model 'Account'
        db.create_table('openbudgetapp_account', (
            ('accountset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.AccountSet'])),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child', null=True, to=orm['openbudgetapp.Account'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal('openbudgetapp', ['Account'])

        # Adding model 'Transaction'
        db.create_table('openbudgetapp_transaction', (
            ('accountset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.AccountSet'])),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('postdate', self.gf('django.db.models.fields.DateField')()),
            ('num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('openbudgetapp', ['Transaction'])

        # Adding model 'AccountExtra'
        db.create_table('openbudgetapp_accountextra', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Account'])),
            ('pct_discrentionary', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=4)),
            ('inflation_category', self.gf('django.db.models.fields.CharField')(default='NONE', max_length=255)),
            ('investment_category', self.gf('django.db.models.fields.CharField')(default='NONE', max_length=255)),
            ('asset_class', self.gf('django.db.models.fields.CharField')(default='NONE', max_length=255)),
        ))
        db.send_create_signal('openbudgetapp', ['AccountExtra'])

        # Adding model 'Client'
        db.create_table('openbudgetapp_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('openbudgetapp', ['Client'])

        # Adding model 'Receipt'
        db.create_table('openbudgetapp_receipt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('postdate', self.gf('django.db.models.fields.DateField')()),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('tx', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Transaction'], null=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Client'], null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('openbudgetapp', ['Receipt'])

        # Adding model 'Project'
        db.create_table('openbudgetapp_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('openbudgetapp', ['Project'])

        # Adding model 'ReceiptExpense'
        db.create_table('openbudgetapp_receiptexpense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('receipt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Receipt'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('allocation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reimbursable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vat', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('paidby', self.gf('django.db.models.fields.CharField')(default='cash', max_length=255)),
        ))
        db.send_create_signal('openbudgetapp', ['ReceiptExpense'])

        # Adding model 'AccountSet'
        db.create_table('openbudgetapp_accountset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('gnucashdb', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
        ))
        db.send_create_signal('openbudgetapp', ['AccountSet'])

    def backwards(self, orm):
        # Deleting model 'Split'
        db.delete_table('openbudgetapp_split')

        # Deleting model 'AccountBudget'
        db.delete_table('openbudgetapp_accountbudget')

        # Deleting model 'InflationRate'
        db.delete_table('openbudgetapp_inflationrate')

        # Deleting model 'Account'
        db.delete_table('openbudgetapp_account')

        # Deleting model 'Transaction'
        db.delete_table('openbudgetapp_transaction')

        # Deleting model 'AccountExtra'
        db.delete_table('openbudgetapp_accountextra')

        # Deleting model 'Client'
        db.delete_table('openbudgetapp_client')

        # Deleting model 'Receipt'
        db.delete_table('openbudgetapp_receipt')

        # Deleting model 'Project'
        db.delete_table('openbudgetapp_project')

        # Deleting model 'ReceiptExpense'
        db.delete_table('openbudgetapp_receiptexpense')

        # Deleting model 'AccountSet'
        db.delete_table('openbudgetapp_accountset')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'openbudgetapp.account': {
            'Meta': {'ordering': "['name']", 'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'accountset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.AccountSet']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child'", 'null': 'True', 'to': "orm['openbudgetapp.Account']"})
        },
        'openbudgetapp.accountbudget': {
            'Meta': {'object_name': 'AccountBudget'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']"}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'estimated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pctnondiscrentionary': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'})
        },
        'openbudgetapp.accountextra': {
            'Meta': {'object_name': 'AccountExtra'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']"}),
            'asset_class': ('django.db.models.fields.CharField', [], {'default': "'NONE'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inflation_category': ('django.db.models.fields.CharField', [], {'default': "'NONE'", 'max_length': '255'}),
            'investment_category': ('django.db.models.fields.CharField', [], {'default': "'NONE'", 'max_length': '255'}),
            'pct_discrentionary': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'})
        },
        'openbudgetapp.accountset': {
            'Meta': {'object_name': 'AccountSet'},
            'gnucashdb': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'openbudgetapp.client': {
            'Meta': {'object_name': 'Client'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'openbudgetapp.inflationrate': {
            'Meta': {'ordering': "['enddate']", 'object_name': 'InflationRate'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'}),
            'startdate': ('django.db.models.fields.DateField', [], {})
        },
        'openbudgetapp.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'openbudgetapp.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Client']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'postdate': ('django.db.models.fields.DateField', [], {}),
            'tx': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Transaction']", 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'openbudgetapp.receiptexpense': {
            'Meta': {'object_name': 'ReceiptExpense'},
            'allocation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paidby': ('django.db.models.fields.CharField', [], {'default': "'cash'", 'max_length': '255'}),
            'receipt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Receipt']"}),
            'reimbursable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'vat': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'openbudgetapp.split': {
            'Meta': {'object_name': 'Split'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']"}),
            'accountset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.AccountSet']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'tx': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Transaction']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'})
        },
        'openbudgetapp.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'accountset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.AccountSet']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'postdate': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['openbudgetapp']