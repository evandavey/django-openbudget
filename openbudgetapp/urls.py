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

  
  (r'^investments/report/(?:(?P<enddate>\d+)/(?P<startdate>\d+)/(?P<format>\w+)/)?$',
		'report',
		None,
		'investment_report'),
)

"""
URLS - Admin
"""
urlpatterns += patterns('openbudgetapp.views.admin',
  (r'^gnucash-import/$', 
  	'gnucash_import',
  	None,
  	'gnucash-import'),
)



if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
