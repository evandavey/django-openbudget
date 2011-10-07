# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Account'
        db.create_table('openbudgetapp_account', (
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Account'])),
        ))
        db.send_create_signal('openbudgetapp', ['Account'])


    def backwards(self, orm):
        
        # Deleting model 'Account'
        db.delete_table('openbudgetapp_account')


    models = {
        'openbudgetapp.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']"})
        }
    }

    complete_apps = ['openbudgetapp']
