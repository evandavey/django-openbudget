# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Transaction'
        db.create_table('openbudgetapp_transaction', (
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('postdate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('openbudgetapp', ['Transaction'])


    def backwards(self, orm):
        
        # Deleting model 'Transaction'
        db.delete_table('openbudgetapp_transaction')


    models = {
        'openbudgetapp.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']", 'null': 'True'})
        },
        'openbudgetapp.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'postdate': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['openbudgetapp']
