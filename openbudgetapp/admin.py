from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from openbudgetapp.models import *

class AccountAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['guid','name','balance','account_type','parent']
	list_filter = ['account_type']
	ordering = ['name']
	search_fields = ['name']


class TransactionAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['guid','postdate','description']
	list_filter = ['postdate']
	ordering = ['postdate']
	search_fields = ['description']


class SplitAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['guid','tx','account','value']
	list_filter = []
	ordering = []
	search_fields = []
	
class AccountBudgetAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['id','account','value','actual']
	list_filter = []
	ordering = []
	search_fields = []

admin.site.register(Account,AccountAdmin)	
admin.site.register(Transaction,TransactionAdmin)	
admin.site.register(Split,SplitAdmin)	
admin.site.register(AccountBudget,AccountBudgetAdmin)	






	
