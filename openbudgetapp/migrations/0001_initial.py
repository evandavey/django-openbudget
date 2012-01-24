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
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child', null=True, to=orm['openbudgetapp.Account'])),
        ))
        db.send_create_signal('openbudgetapp', ['Account'])

        # Adding model 'Transaction'
        db.create_table('openbudgetapp_transaction', (
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('postdate', self.gf('django.db.models.fields.DateField')()),
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
        'openbudgetapp.inflationrate': {
            'Meta': {'ordering': "['enddate']", 'object_name': 'InflationRate'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'}),
            'startdate': ('django.db.models.fields.DateField', [], {})
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
