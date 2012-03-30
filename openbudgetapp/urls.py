from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from django.conf import settings
from openbudgetapp.models import Account

urlpatterns = patterns('',
(r'^$','openbudgetapp.views.index'),
(r'^budget/(?P<startdate>\d+)/(?P<enddate>\d+)/(?P<depth>\d+)/(?P<method>\w+)/$','openbudgetapp.views.budget_report'),

)


"""
URLS - Investment
"""
urlpatterns += patterns('openbudgetapp.views.investments',

  
  (r'^(?P<accountset_id>\d+)/investments/report/(?:(?P<enddate>\d+)/(?P<startdate>\d+)/(?P<format>\w+)/)?$',
		'report',
		None,
		'investment_report'),
)

"""
URLS - Business
"""
urlpatterns += patterns('openbudgetapp.views.business',

  
  (r'^(?P<accountset_id>\d+)/business/transaction_journal/?$',
		'transaction_journal',
		None,
		'transaction_journal'),
)

"""
URLS - Admin
"""
urlpatterns += patterns('openbudgetapp.views.admin',
  (r'^gnucash-import/(?P<accountset_id>\d+)/$', 
  	'gnucash_import',
  	None,
  	'gnucash-import'),
  	
  	(r'^redmine-import/(?P<accountset_id>\d+)/$', 
     	'redmine_import',
     	None,
     	'redmine-import'),
)

"""
API
"""
from tastypie.api import Api
from openbudgetapp.api import *

v1_api = Api(api_name='v1')
v1_api.register(TransactionResource(), canonical=True)
v1_api.register(AccountSetResource(), canonical=True)

urlpatterns += patterns('',
    (r'^api/', include(v1_api.urls)),
)


