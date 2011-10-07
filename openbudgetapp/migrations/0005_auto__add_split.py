# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Split'
        db.create_table('openbudgetapp_split', (
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('tx', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Transaction'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Account'])),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=4)),
        ))
        db.send_create_signal('openbudgetapp', ['Split'])


    def backwards(self, orm):
        
        # Deleting model 'Split'
        db.delete_table('openbudgetapp_split')


    models = {
        'openbudgetapp.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']", 'null': 'True'})
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
