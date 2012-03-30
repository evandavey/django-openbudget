# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
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

        # Adding model 'Client'
        db.create_table('openbudgetapp_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('openbudgetapp', ['Client'])


    def backwards(self, orm):
        
        # Deleting model 'Receipt'
        db.delete_table('openbudgetapp_receipt')

        # Deleting model 'Project'
        db.delete_table('openbudgetapp_project')

        # Deleting model 'Client'
        db.delete_table('openbudgetapp_client')


    models = {
        'openbudgetapp.account': {
            'Meta': {'ordering': "['name']", 'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
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
        'openbudgetapp.split': {
            'Meta': {'object_name': 'Split'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'tx': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Transaction']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'})
        },
        'openbudgetapp.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'postdate': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['openbudgetapp']
