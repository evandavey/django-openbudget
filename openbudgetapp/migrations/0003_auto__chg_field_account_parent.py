# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Account.parent'
        db.alter_column('openbudgetapp_account', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openbudgetapp.Account'], null=True))


    def backwards(self, orm):
        
        # Changing field 'Account.parent'
        db.alter_column('openbudgetapp_account', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['openbudgetapp.Account']))


    models = {
        'openbudgetapp.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openbudgetapp.Account']", 'null': 'True'})
        }
    }

    complete_apps = ['openbudgetapp']
