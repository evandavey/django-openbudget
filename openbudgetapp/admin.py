from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from openbudgetapp.models import *

class AccountAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['guid','name','balance','account_type','parent','inflationrate']
	list_filter = ['account_type','accountset']
	ordering = ['name']
	search_fields = ['name']


class TransactionAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['guid','postdate','description','num']
	list_filter = ['postdate','accountset']
	ordering = ['postdate']
	search_fields = ['description']


class SplitAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['guid','tx','account','value']
	list_filter = ['accountset']
	ordering = []
	search_fields = []
	
class AccountBudgetAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['id','enddate','account','estimated','pctnondiscrentionary','value','actual']
	list_filter = ['account','enddate']
	ordering = ['enddate','account']
	search_fields = []



class AccountExtraAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['id','account',]
	list_filter = []
	ordering = []
	search_fields = []	


class InflationRateAdmin(admin.ModelAdmin):
	""" Object to control the behaviour of the linked object in the Admin interface
	"""
	list_display = ['category','enddate','rate',]
	list_filter = ['category','enddate']
	ordering = ['enddate','category']
	search_fields = []


class AccountSetAdmin(admin.ModelAdmin):
    """ Object to control the behaviour of the linked object in the Admin interface
    """
    list_display = ['name','style',]
    list_filter = ['name']

class ReceiptAdmin(admin.ModelAdmin):
    """ Object to control the behaviour of the linked object in the Admin interface
    """
    list_display = ['postdate','url',]

class ClientAdmin(admin.ModelAdmin):
    """ Object to control the behaviour of the linked object in the Admin interface
    """
    list_display = ['firstname','lastname','company']

admin.site.register(Account,AccountAdmin)	
admin.site.register(Transaction,TransactionAdmin)	
admin.site.register(Split,SplitAdmin)	
admin.site.register(AccountBudget,AccountBudgetAdmin)	
admin.site.register(AccountExtra,AccountExtraAdmin)	
admin.site.register(InflationRate,InflationRateAdmin)	
admin.site.register(AccountSet,AccountSetAdmin)	
admin.site.register(Client,ClientAdmin)	
admin.site.register(Receipt,ReceiptAdmin)	
admin.site.register(ReceiptExpense)	






	
